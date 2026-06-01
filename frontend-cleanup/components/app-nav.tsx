"use client";
import Link from "next/link";
import { usePathname } from "next/navigation";

const links = [
  ["Dashboard", "/"],
  ["Deals", "/deals"],
  ["Market research", "/market-research"],
  ["Settings", "/settings"],
];

export function AppNav() {
  const pathname = usePathname();
  return (
    <nav className="app-nav" aria-label="Main navigation">
      {links.map(([label, href]) => (
        <Link
          href={href}
          key={href}
          className={pathname === href ? "nav-active" : ""}
        >
          {label}
        </Link>
      ))}
    </nav>
  );
}
