import type { Metadata } from 'next';
import './globals.css';
export const metadata: Metadata = {
  title: { default: 'Arduino · Design & Technik', template: '%s · Arduino' },
  description:
    'Arduino im Unterricht: Einrichtung, Programmierung, Sensoren, Aktoren und kreative Projekte. Von Lukas Jordi.',
};
export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="de-CH">
      <body>{children}</body>
    </html>
  );
}
