import { notFound } from 'next/navigation';
import Site from '../site';
import pages from '../content.json';
export function generateStaticParams() {
  return pages.map((p) => ({ slug: p.slug }));
}
export async function generateMetadata({
  params,
}: {
  params: Promise<{ slug: string }>;
}) {
  const { slug } = await params;
  const page = pages.find((p) => p.slug === slug);
  return { title: page?.title || 'Seite nicht gefunden' };
}
export default async function ContentPage({
  params,
}: {
  params: Promise<{ slug: string }>;
}) {
  const { slug } = await params;
  const page = pages.find((p) => p.slug === slug);
  if (!page) notFound();
  return <Site page={page} />;
}
