"use client"

import { Navbar } from "@/components/navbar"
import { motion } from "framer-motion"
import { ArrowRight, Sparkles, Video, Mic, FileText, Layout, Layers, Zap, Clock, Trash2, GalleryVerticalEnd } from "lucide-react"
import { Button } from "@/components/ui/button"
import Link from "next/link"

const fadeIn = {
  initial: { opacity: 0, y: 20 },
  animate: { opacity: 1, y: 0 },
  transition: { duration: 0.6 }
}

const steps = [
  {
    icon: <FileText className="size-6 text-primary" />,
    title: "AI Script Generation",
    description: "Our AI generates a cinematic script with precise narration and visual keywords tailored to your topic."
  },
  {
    icon: <Layers className="size-6 text-primary" />,
    title: "Asset Selection",
    description: "Automated fetching of high-quality images and video clips that perfectly match the script's visual cues."
  },
  {
    icon: <Mic className="size-6 text-primary" />,
    title: "Pro Voiceovers",
    description: "High-fidelity text-to-speech engine produces realistic narration with natural pacing and emotion."
  },
  {
    icon: <Layout className="size-6 text-primary" />,
    title: "Automated Assembly",
    description: "Seamlessly merging all assets, audio, and visuals into a final production-ready video."
  }
]

const features = [
  {
    icon: <Zap className="size-5 text-purple-400" />,
    title: "Instant Processing",
    description: "Generate complete videos in minutes, not hours. Save time on editing and focus on content strategy."
  },
  {
    icon: <Video className="size-5 text-blue-400" />,
    title: "Real Assets",
    description: "No AI hallucinations. We use real, high-quality images and videos for a authentic viewer experience."
  },
  {
    icon: <Clock className="size-5 text-green-400" />,
    title: "Perfect Pacing",
    description: "Visuals are automatically synchronized to exactly match the duration of the narration."
  }
]

export default function LandingPage() {
  return (
    <div className="min-h-screen bg-background text-foreground overflow-x-hidden">
      <Navbar />

      {/* Hero Section */}
      <section className="relative pt-32 pb-20 md:pt-48 md:pb-32 container mx-auto px-4 text-center overflow-hidden">
        {/* Background Gradients */}
        <div className="absolute top-0 left-1/2 -translate-x-1/2 w-full h-[600px] bg-primary/20 blur-[120px] rounded-[50%] -z-10 opacity-30 select-none pointer-events-none" />
        <div className="absolute top-40 right-0 w-[300px] h-[300px] bg-purple-500/10 blur-[100px] rounded-full -z-10 select-none pointer-events-none" />
        
        <motion.div {...fadeIn} className="flex flex-col items-center gap-6 max-w-4xl mx-auto">
          <div className="inline-flex items-center gap-2 px-3 py-1 rounded-full border border-primary/20 bg-primary/5 text-primary text-xs font-semibold backdrop-blur-sm animate-pulse-slow">
            <Sparkles className="size-3" />
            <span>Automate your video production with AI</span>
          </div>
          
          <h1 className="text-5xl md:text-7xl lg:text-8xl font-black tracking-tight leading-[0.9] text-transparent bg-clip-text bg-gradient-to-b from-foreground via-foreground to-foreground/40 pb-2">
            Automate Your <br />
            Content <span className="text-primary italic">Engine</span>
          </h1>
          
          <p className="text-lg md:text-xl text-muted-foreground leading-relaxed max-w-2xl">
            Turn simple text into professional-grade videos using automated assembly of high-quality assets, 
            realistic voiceovers, and AI-driven scripts. No manual editing required.
          </p>
          
          <div className="flex flex-col sm:flex-row items-center gap-4 mt-4">
            <Link href="/chat">
              <Button size="lg" className="h-14 px-8 rounded-full text-lg font-bold shadow-2xl shadow-primary/30 cursor-pointer">
                Start Generating <ArrowRight className="ml-2 size-5" />
              </Button>
            </Link>
            <Button size="lg" variant="outline" className="h-14 px-8 rounded-full text-lg font-bold border-foreground/10 bg-foreground/5 backdrop-blur-sm hover:bg-foreground/10 cursor-pointer">
              Watch Demo
            </Button>
          </div>
        </motion.div>

        {/* Hero Visual Mockup */}
        <motion.div 
            initial={{ opacity: 0, y: 40 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: 0.3, duration: 0.8 }}
            className="mt-16 md:mt-24 relative max-w-5xl mx-auto"
        >
            <div className="relative rounded-2xl border border-white/10 bg-zinc-900/50 p-2 shadow-2xl overflow-hidden group">
                <div className="absolute inset-0 bg-gradient-to-t from-zinc-950 via-transparent h-full z-10 opacity-60" />
                <div className="absolute inset-0 flex items-center justify-center z-20 opacity-0 group-hover:opacity-100 transition-opacity">
                    <div className="size-16 rounded-full bg-primary/90 flex items-center justify-center text-primary-foreground shadow-2xl scale-90 group-hover:scale-100 transition-transform cursor-pointer">
                        <Video className="size-7 fill-current" />
                    </div>
                </div>
                <div className="aspect-video w-full rounded-xl bg-zinc-950 overflow-hidden relative">
                   <div className="absolute inset-0 bg-[radial-gradient(circle_at_center,_var(--zinc-800)_0%,_transparent_100%)] opacity-20" />
                    <div className="absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 grid grid-cols-3 gap-4 w-[150%] max-w-4xl rotate-12 opacity-40">
                       {[...Array(9)].map((_, i) => (
                           <div key={i} className="aspect-video rounded-lg border border-white/10 bg-zinc-900 shadow-xl" />
                       ))}
                    </div>
                    {/* UI Overlay Mockup */}
                    <div className="absolute top-4 left-4 z-10 flex gap-2">
                        <div className="h-2 w-8 rounded-full bg-primary/60" />
                        <div className="h-2 w-4 rounded-full bg-white/20" />
                        <div className="h-2 w-4 rounded-full bg-white/10" />
                    </div>
                    <div className="absolute bottom-6 left-6 z-10 max-w-xs space-y-2">
                        <div className="h-4 w-40 rounded-md bg-white/20" />
                        <div className="h-3 w-64 rounded-md bg-white/10" />
                        <div className="h-3 w-32 rounded-md bg-white/10" />
                    </div>
                </div>
            </div>
            {/* Float Elements */}
            <div className="absolute -top-6 -right-6 px-4 py-2 rounded-xl border border-white/10 bg-zinc-900 shadow-xl z-20 backdrop-blur-md hidden md:flex items-center gap-2">
                <Layout className="size-4 text-primary" />
                <span className="text-xs font-bold">Smart Assembly</span>
            </div>
            <div className="absolute -bottom-6 -left-6 px-4 py-2 rounded-xl border border-white/10 bg-zinc-900 shadow-xl z-20 backdrop-blur-md hidden md:flex items-center gap-2">
                <Zap className="size-4 text-purple-400" />
                <span className="text-xs font-bold">Rendered in 45s</span>
            </div>
        </motion.div>
      </section>

      {/* Process Section */}
      <section id="how-it-works" className="py-20 md:py-32 relative">
        <div className="container mx-auto px-4">
          <div className="text-center mb-16 space-y-4">
            <h2 className="text-3xl md:text-5xl font-bold tracking-tight">How NovaMind works</h2>
            <p className="text-muted-foreground max-w-xl mx-auto">
              Our sophisticated pipeline handles everything from orchestration to final rendering.
            </p>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-8">
            {steps.map((step, i) => (
              <motion.div
                key={i}
                initial={{ opacity: 0, y: 20 }}
                whileInView={{ opacity: 1, y: 0 }}
                viewport={{ once: true }}
                transition={{ delay: i * 0.1 }}
                className="group p-6 rounded-2xl border border-foreground/5 bg-foreground/[0.02] hover:bg-foreground/[0.04] transition-all relative"
              >
                  <div className="absolute top-6 right-6 text-4xl font-black text-foreground/5 italic select-none">
                    0{i+1}
                  </div>
                <div className="size-12 rounded-xl bg-primary/10 flex items-center justify-center mb-6 border border-primary/20 group-hover:scale-110 transition-transform">
                  {step.icon}
                </div>
                <h3 className="text-xl font-bold mb-3">{step.title}</h3>
                <p className="text-sm text-muted-foreground leading-relaxed">
                  {step.description}
                </p>
              </motion.div>
            ))}
          </div>
        </div>
      </section>

      {/* Features Section */}
      <section id="features" className="py-20 md:py-32 bg-foreground/[0.02] border-y border-foreground/5 relative">
        <div className="container mx-auto px-4 grid grid-cols-1 lg:grid-cols-2 gap-16 items-center">
            <div className="space-y-8">
                <div className="space-y-4">
                    <h2 className="text-3xl md:text-5xl font-bold tracking-tight leading-tight">
                        Content creation at the <br />
                        speed of <span className="text-primary italic">thought</span>
                    </h2>
                    <p className="text-muted-foreground text-lg leading-relaxed">
                        NovaMind isn't just another generative AI. It's a professional orchestration engine 
                        that selects and assembles the best human-shot assets for your story.
                    </p>
                </div>
                
                <div className="space-y-6">
                    {features.map((f, i) => (
                        <div key={i} className="flex gap-4 p-4 rounded-xl border border-foreground/5 hover:border-foreground/10 transition-colors bg-foreground/[0.02]">
                            <div className="size-10 shrink-0 rounded-lg bg-foreground/5 flex items-center justify-center">
                                {f.icon}
                            </div>
                            <div>
                                <h4 className="font-bold text-lg mb-1">{f.title}</h4>
                                <p className="text-sm text-muted-foreground leading-relaxed">{f.description}</p>
                            </div>
                        </div>
                    ))}
                </div>
            </div>

            <div className="relative aspect-square md:aspect-[4/5] rounded-3xl border border-foreground/10 bg-background/50 backdrop-blur-xl p-8 overflow-hidden shadow-2xl">
                <div className="absolute top-0 left-0 w-full h-full bg-gradient-to-br from-primary/10 via-transparent to-transparent opacity-50" />
                
                <div className="relative z-10 h-full flex flex-col justify-between">
                    <div className="space-y-6">
                        <div className="px-6 py-4 rounded-xl border border-foreground/10 bg-background shadow-2xl space-y-3">
                            <div className="flex items-center gap-2">
                                <div className="size-2 rounded-full bg-green-500" />
                                <span className="text-[10px] font-bold uppercase tracking-widest text-foreground/50">Script Active</span>
                            </div>
                            <h5 className="text-sm font-bold">Sustainable Fashion in 2026</h5>
                            <p className="text-[11px] text-muted-foreground leading-relaxed">
                                "In an era where every choice counts, sustainable fashion is no longer a luxury..."
                            </p>
                        </div>

                        <div className="translate-x-12 px-6 py-4 rounded-xl border border-primary/20 bg-primary/5 shadow-2xl backdrop-blur-md space-y-4">
                             <div className="flex items-center justify-between text-[10px] font-bold uppercase tracking-widest">
                                <span className="text-primary">Voice Syncing</span>
                                <span>85%</span>
                            </div>
                            <div className="h-1.5 w-full bg-primary/10 rounded-full overflow-hidden">
                                <div className="h-full w-[85%] bg-primary" />
                            </div>
                        </div>

                        <div className="px-6 py-4 rounded-xl border border-foreground/10 bg-background shadow-2xl flex items-center gap-4">
                            <div className="size-10 rounded bg-foreground/5" />
                            <div className="flex-1 space-y-1.5">
                                <div className="h-2 w-20 bg-foreground/10 rounded-full" />
                                <div className="h-1.5 w-full bg-foreground/5 rounded-full" />
                            </div>
                        </div>
                    </div>

                    <div className="mt-8">
                         <div className="w-full aspect-video rounded-xl bg-background border border-foreground/10 shadow-3xl relative flex items-center justify-center">
                            <GalleryVerticalEnd className="size-10 text-primary opacity-20" />
                            <div className="absolute inset-0 bg-gradient-to-t from-primary/5 to-transparent" />
                         </div>
                    </div>
                </div>
            </div>
        </div>
      </section>

      {/* CTA Section */}
      <section className="py-20 md:py-40 container mx-auto px-4 text-center">
        <motion.div 
            initial={{ opacity: 0, scale: 0.95 }}
            whileInView={{ opacity: 1, scale: 1 }}
            viewport={{ once: true }}
            transition={{ duration: 0.8 }}
            className="p-10 md:p-20 rounded-[3rem] border border-primary/20 bg-gradient-to-br from-primary/20 via-primary/5 to-primary/0 relative overflow-hidden"
        >
            <div className="absolute inset-0 bg-[radial-gradient(circle_at_top_right,_var(--primary)_0%,_transparent_50%)] opacity-10" />
            
            <div className="relative z-10 space-y-8 max-w-3xl mx-auto">
                <h2 className="text-4xl md:text-6xl font-black leading-tight tracking-tight">
                    Ready to build your content <span className="italic">empire</span>?
                </h2>
                <p className="text-muted-foreground text-lg md:text-xl">
                    Join professional creators who use NovaMind to automate their visual storytelling 
                    without sacrificing quality or authenticity.
                </p>
                <div className="flex flex-col sm:flex-row items-center justify-center gap-4 pt-4">
                     <Link href="/chat">
                        <Button size="lg" className="h-14 px-10 rounded-full text-lg font-bold shadow-2xl shadow-primary/40 cursor-pointer">
                            Start Generating Now
                        </Button>
                     </Link>
                    <Button variant="outline" size="lg" className="h-14 px-10 rounded-full text-lg font-bold bg-transparent border-white/10 hover:bg-white/5 cursor-pointer">
                        View Pricing
                    </Button>
                </div>
            </div>
        </motion.div>
      </section>

      {/* Footer */}
      <footer className="py-12 border-t border-foreground/5 bg-background">
        <div className="container mx-auto px-4 flex flex-col md:flex-row items-center justify-between gap-8">
            <Link href="/" className="flex items-center gap-2.5">
                <div className="flex aspect-square size-6 items-center justify-center rounded-md bg-primary text-primary-foreground">
                    <GalleryVerticalEnd className="size-3" />
                </div>
                <span className="text-lg font-bold tracking-tight">NovaMind</span>
            </Link>

            <div className="flex items-center gap-8 text-sm text-muted-foreground font-medium">
                <Link href="#" className="hover:text-foreground transition-colors">Privacy</Link>
                <Link href="#" className="hover:text-foreground transition-colors">Terms</Link>
                <Link href="#" className="hover:text-foreground transition-colors">Twitter</Link>
                <Link href="#" className="hover:text-foreground transition-colors">Discord</Link>
            </div>

            <p className="text-sm text-muted-foreground">
                © 2026 NovaMind Video Engine.
            </p>
        </div>
      </footer>
    </div>
  )
}
