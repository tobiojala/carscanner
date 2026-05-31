import Link from "next/link";

const links = [
  ["Dashboard", "/"],
  ["Deal scanner", "/deals"],
  ["Link intake", "/link-intake"],
  ["Pipeline", "/pipeline"],
  ["Market research", "/market-research"],
  ["Settings", "/settings"]
];

export function AppNav() {
  return (
    <nav className="app-nav" aria-label="Main navigation">
      {links.map(([label, href]) => (
        <Link href={href} key={href}>
          {label}
        </Link>
      ))}
    </nav>
  );
}
