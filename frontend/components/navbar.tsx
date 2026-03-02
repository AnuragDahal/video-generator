"use client"

import Link from "next/link"
import { GalleryVerticalEnd } from "lucide-react"
import { Button } from "@/components/ui/button"

export function Navbar() {
  return (
    <nav className="fixed top-0 left-0 right-0 z-50 border-b border-white/5 bg-background/80 backdrop-blur-xl">
      <div className="container mx-auto px-4 h-16 flex items-center justify-between">
        <Link href="/" className="flex items-center gap-2.5 group">
          <div className="flex aspect-square size-8 items-center justify-center rounded-lg bg-primary text-primary-foreground transition-transform group-hover:scale-105">
            <GalleryVerticalEnd className="size-4" />
          </div>
          <span className="text-xl font-bold tracking-tight text-foreground">NovaMind</span>
        </Link>

        <div className="hidden md:flex items-center gap-8">
          <Link href="#features" className="text-sm font-medium text-muted-foreground hover:text-foreground transition-colors">
            Features
          </Link>
          <Link href="#how-it-works" className="text-sm font-medium text-muted-foreground hover:text-foreground transition-colors">
            Process
          </Link>
          <Link href="#showcase" className="text-sm font-medium text-muted-foreground hover:text-foreground transition-colors">
            Showcase
          </Link>
        </div>

        <div className="flex items-center gap-4">
          <Link href="/chat">
            <Button variant="ghost" className="text-sm font-medium hidden sm:flex cursor-pointer">
              Login
            </Button>
          </Link>
          <Link href="/chat">
            <Button className="bg-primary hover:bg-primary/90 text-primary-foreground shadow-lg shadow-primary/20 cursor-pointer">
              Start Generating
            </Button>
          </Link>
        </div>
      </div>
    </nav>
  )
}
