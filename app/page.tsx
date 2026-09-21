import Site from './site';
import pages from './content.json';
export default function Home() {
  return <Site page={pages[0]} />;
}
