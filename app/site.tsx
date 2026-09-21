'use client';
/* Native local images avoid a server image optimizer. Focusable code regions allow keyboard scrolling,
   and autofocus follows an explicit search action. execCommand supports embedded browsers. */
/* oxlint-disable next/no-img-element, jsx-a11y/no-noninteractive-tabindex, jsx-a11y/no-autofocus, typescript/no-deprecated, next/no-html-link-for-pages */
import { useEffect, useState } from 'react';
import { Search, X, Copy, Check, Menu, Play } from 'lucide-react';
import {
  Sidebar,
  SidebarContent,
  SidebarHeader,
  SidebarProvider,
  useSidebar,
} from '@/components/ui/sidebar';
import {
  Accordion,
  AccordionItem,
  AccordionTrigger,
  AccordionContent,
} from '@/components/ui/accordion';
import rawPages from './content.json';
import { BreadboardGuide } from './breadboard-guide';

type Block = {
  type: string;
  id?: string;
  marker?: string;
  diagram?: string;
  label?: string;
  html?: string;
  code?: string;
  src?: string;
  alt?: string;
  href?: string;
  title?: string;
  source?: string;
  width?: number;
  height?: number;
};
type Section = {
  id: string;
  accordion: boolean;
  title: string;
  anchor: string;
  gallery: boolean;
  layout?: string;
  cells: { blocks: Block[] }[];
};
type Page = { slug: string; label: string; title: string; sections: Section[] };
const pages: Page[] = rawPages;
function CodeBlock({ code, label }: { code: string; label?: string }) {
  const [state, setState] = useState<'idle' | 'copied' | 'error'>('idle');
  async function copy() {
    // Webviews may leave the asynchronous Clipboard API pending. Copy during
    // the click's user gesture first, then use the modern API as a fallback.
    let success = false;
    const focused = document.activeElement as HTMLElement | null;
    const field = document.createElement('textarea');
    field.value = code;
    field.style.position = 'fixed';
    field.style.top = '0';
    field.style.left = '0';
    field.style.opacity = '0';
    field.setAttribute('readonly', '');
    document.body.appendChild(field);
    field.select();
    field.setSelectionRange(0, code.length);
    try {
      success = document.execCommand('copy');
    } catch {
      success = false;
    } finally {
      field.remove();
      focused?.focus({ preventScroll: true });
    }
    if (!success && navigator.clipboard && window.isSecureContext) {
      try {
        await navigator.clipboard.writeText(code);
        success = true;
      } catch {}
    }
    setState(success ? 'copied' : 'error');
    window.setTimeout(() => setState('idle'), 2500);
  }
  const tokens = code.split(
    /(\/\/[^\n]*|"(?:\\.|[^"\\])*"|'(?:\\.|[^'\\])*'|#[a-z]+|\b(?:void|int|long|unsigned|const|bool|float|char|static|if|else|for|while|return|true|false|HIGH|LOW|OUTPUT|INPUT_PULLUP|INPUT)\b|\b\d+(?:\.\d+)?\b)/g,
  );
  return (
    <div className="code-block">
      <div className="code-toolbar">
        <span>{label || 'Arduino / C++'}</span>
        <button onClick={copy} type="button" aria-label="Code kopieren">
          {state === 'copied' ? <Check size={15} /> : <Copy size={15} />}
          <span aria-live="polite">
            {state === 'copied'
              ? 'Kopiert!'
              : state === 'error'
                ? 'Bitte Code markieren'
                : 'Code kopieren'}
          </span>
        </button>
      </div>
      <pre tabIndex={0} aria-label="Arduino-Code">
        <code>
          {tokens.map((token, i) => (
            <span
              key={i}
              className={
                token.startsWith('//')
                  ? 'code-comment'
                  : token.startsWith('"') || token.startsWith("'")
                    ? 'code-string'
                    : /^\d/.test(token)
                      ? 'code-number'
                      : /^(#|void$|int$|long$|unsigned$|const$|bool$|float$|char$|static$|if$|else$|for$|while$|return$|true$|false$|HIGH$|LOW$|OUTPUT$|INPUT)/.test(
                            token,
                          )
                        ? 'code-keyword'
                        : undefined
              }
            >
              {token}
            </span>
          ))}
        </code>
      </pre>
    </div>
  );
}
function Video({ block }: { block: Block }) {
  const [loaded, setLoaded] = useState(false);
  return (
    <div className="video-block">
      {loaded ? (
        <iframe
          src={block.src}
          title={block.title}
          allow="fullscreen"
          allowFullScreen
        />
      ) : (
        <button onClick={() => setLoaded(true)} className="video-load">
          <Play size={30} />
          <span>Projektvideo abspielen</span>
          <small>Video von SWITCHtube laden</small>
        </button>
      )}
    </div>
  );
}
function Blocks({ blocks }: { blocks: Block[] }) {
  return (
    <>
      {blocks.map((b, i) =>
        b.type === 'didactic' ? (
          <aside
            key={i}
            id={b.id}
            className="didactic-note"
            aria-labelledby={b.id + '-title'}
          >
            <p className="didactic-marker">
              Didaktische Ergänzung · {b.marker}
            </p>
            <p className="didactic-title" id={b.id + '-title'}>
              {b.title}
            </p>
            {b.diagram === 'breadboard' && <BreadboardGuide />}
            <div
              className="prose-content"
              dangerouslySetInnerHTML={{ __html: b.html! }}
            />
          </aside>
        ) : b.type === 'code' ? (
          <CodeBlock key={i} code={b.code!} label={b.label} />
        ) : b.type === 'html' ? (
          <div
            key={i}
            className="prose-content"
            dangerouslySetInnerHTML={{ __html: b.html! }}
          />
        ) : b.type === 'image' ? (
          <figure key={i}>
            {b.href ? (
              <a href={b.href}>
                <img
                  src={b.src}
                  alt={b.alt}
                  width={b.width}
                  height={b.height}
                  loading="lazy"
                />
              </a>
            ) : (
              <img
                src={b.src}
                alt={b.alt}
                width={b.width}
                height={b.height}
                loading="lazy"
              />
            )}
          </figure>
        ) : b.type === 'video' ? (
          <Video key={i} block={b} />
        ) : null,
      )}
    </>
  );
}
function Navigation({ page }: { page: Page }) {
  return (
    <Sidebar className="site-sidebar">
      <SidebarHeader className="brand">
        <a href="/home">ARDUINO</a>
      </SidebarHeader>
      <SidebarContent>
        <nav className="site-navigation" aria-label="Hauptnavigation">
          {pages.map((p) => (
            <a
              key={p.slug}
              href={'/' + p.slug}
              aria-current={p.slug === page.slug ? 'page' : undefined}
            >
              {p.label}
            </a>
          ))}
        </nav>
      </SidebarContent>
    </Sidebar>
  );
}
function MobileMenu() {
  const { toggleSidebar } = useSidebar();
  return (
    <button
      className="mobile-menu icon-button"
      onClick={toggleSidebar}
      aria-label="Navigation öffnen"
    >
      <Menu size={23} />
    </button>
  );
}
export default function Site({ page }: { page: Page }) {
  const [searchOpen, setSearchOpen] = useState(false),
    [query, setQuery] = useState(''),
    [expanded, setExpanded] = useState<string[]>([]);
  useEffect(() => {
    const openAnchor = () => {
      const hash = decodeURIComponent(window.location.hash.slice(1));
      if (!hash) return;
      const section = page.sections.find(
        (s) =>
          s.anchor === hash ||
          s.id === hash ||
          s.cells.some((c) =>
            c.blocks.some(
              (b) => b.id === hash || b.html?.includes('id="' + hash + '"'),
            ),
          ),
      );
      if (section?.accordion)
        setExpanded((v) => (v.includes(section.id) ? v : [...v, section.id]));
      window.setTimeout(
        () => document.getElementById(hash)?.scrollIntoView({ block: 'start' }),
        100,
      );
    };
    openAnchor();
    window.addEventListener('hashchange', openAnchor);
    return () => window.removeEventListener('hashchange', openAnchor);
  }, [page]);
  const terms = query.toLocaleLowerCase('de').trim();
  const results = terms
    ? pages.flatMap((p) =>
        p.sections
          .filter((s) =>
            (
              s.title +
              ' ' +
              s.cells
                .flatMap((c) =>
                  c.blocks.map(
                    (b) =>
                      (b.title || '') +
                      ' ' +
                      (b.html?.replace(/<[^>]*>/g, ' ') || b.code || ''),
                  ),
                )
                .join(' ')
            )
              .toLocaleLowerCase('de')
              .includes(terms),
          )
          .map((s) => ({
            label: p.label,
            title: s.title || p.title,
            href: '/' + p.slug + (s.anchor ? '#' + s.anchor : ''),
          })),
      )
    : [];
  return (
    <SidebarProvider
      style={{ '--sidebar-width': '248px' } as React.CSSProperties}
    >
      <a href="#main" className="skip-link">
        Zum Inhalt springen
      </a>
      <Navigation page={page} />
      <div className="site-main">
        <header className="utility-bar">
          <MobileMenu />
          <button
            className="icon-button search-toggle"
            aria-label={searchOpen ? 'Suche schliessen' : 'Website durchsuchen'}
            aria-expanded={searchOpen}
            onClick={() => setSearchOpen((v) => !v)}
          >
            {searchOpen ? <X size={22} /> : <Search size={22} />}
          </button>
        </header>
        {searchOpen && (
          <section className="site-search" aria-label="Website durchsuchen">
            <label htmlFor="search-input">Website durchsuchen</label>
            <input
              id="search-input"
              type="search"
              autoFocus
              value={query}
              onChange={(e) => setQuery(e.target.value)}
              placeholder="Suchbegriff eingeben …"
              onKeyDown={(e) => {
                if (e.key === 'Escape') setSearchOpen(false);
              }}
            />
            {terms && (
              <>
                <output className="search-count">
                  {results.length} Treffer
                </output>
                <ul>
                  {results.map((r, i) => (
                    <li key={i}>
                      <a
                        href={r.href}
                        onClick={() => {
                          setSearchOpen(false);
                          setQuery('');
                        }}
                      >
                        <strong>{r.title}</strong>
                        <span>{r.label}</span>
                      </a>
                    </li>
                  ))}
                </ul>
              </>
            )}
          </section>
        )}
        <main id="main" className={'article page-' + page.slug}>
          <Accordion
            multiple
            value={expanded}
            onValueChange={(v) => setExpanded(v as string[])}
          >
            {page.sections.map((s) =>
              s.accordion ? (
                <AccordionItem
                  key={s.id}
                  value={s.id}
                  id={s.anchor || s.id}
                  className="lesson"
                >
                  <AccordionTrigger className="lesson-title">
                    <span className="lesson-heading">
                      <span>{s.title}</span>
                      {s.cells.some((c) =>
                        c.blocks.some((b) => b.type === 'didactic'),
                      ) && (
                        <span className="didactic-lesson-badge">
                          Didaktisch ergänzt
                        </span>
                      )}
                    </span>
                  </AccordionTrigger>
                  <AccordionContent className="lesson-content">
                    {s.cells.map((c, i) => (
                      <div className="content-cell" key={i}>
                        <Blocks blocks={c.blocks} />
                      </div>
                    ))}
                  </AccordionContent>
                </AccordionItem>
              ) : (
                <section
                  key={s.id}
                  id={s.id}
                  className={
                    'content-section' +
                    (s.gallery ? ' image-gallery' : '') +
                    (s.layout ? ' ' + s.layout : '')
                  }
                  style={
                    s.gallery
                      ? ({ '--columns': s.cells.length } as React.CSSProperties)
                      : undefined
                  }
                >
                  {s.cells.map((c, i) => (
                    <div className="content-cell" key={i}>
                      <Blocks blocks={c.blocks} />
                    </div>
                  ))}
                </section>
              ),
            )}
          </Accordion>
        </main>
      </div>
    </SidebarProvider>
  );
}
