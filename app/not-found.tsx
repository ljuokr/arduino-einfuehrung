/* oxlint-disable next/no-html-link-for-pages -- Static pages use direct browser navigation. */
export default function NotFound() {
  return (
    <main className="not-found">
      <h1>Seite nicht gefunden</h1>
      <p>Diese Seite gibt es hier nicht.</p>
      <a href="/home">Zur Startseite</a>
    </main>
  );
}
