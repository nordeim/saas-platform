import type { Metadata } from 'next';
import { Inter } from 'next/font/google';
import './globals.css';

const inter = Inter({ subsets: ['latin'] });

export const metadata: Metadata = {
  title: 'NexusCore - Singapore B2B SaaS Platform',
  description: 'Professional B2B SaaS platform with Singapore GST compliance and PDPA automation.',
  keywords: ['SaaS', 'Singapore', 'GST', 'PDPA', 'B2B'],
  authors: [{ name: 'NexusCore Team', url: 'https://nexuscore.sg' }],
  creator: 'NexusCore',
  publisher: 'NexusCore',
  robots: 'index, follow',
  openGraph: {
    title: 'NexusCore - Singapore B2B SaaS Platform',
    description: 'Professional B2B SaaS platform with Singapore GST compliance and PDPA automation.',
    type: 'website',
    locale: 'en_SG',
    siteName: 'NexusCore',
  },
  twitter: {
    card: 'summary_large_image',
    title: 'NexusCore - Singapore B2B SaaS Platform',
    description: 'Professional B2B SaaS platform with Singapore GST compliance and PDPA automation.',
  },
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="en" className={inter.className}>
      <body>{children}</body>
    </html>
  );
}