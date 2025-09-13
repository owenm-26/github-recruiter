"use client"

import Header from "@/components/layout/Header"
import Footer from "@/components/layout/Footer"
import { Button } from "@/components/ui/button"
import { useRouter } from "next/navigation"


export default function Home() {
  const router = useRouter()

  return (
    <div className="font-sans grid grid-rows-[20px_1fr_20px] items-center justify-items-center min-h-screen p-8 pb-20 gap-16 sm:p-20">
      <Header />

      <div className="text-center space-y-8">
        <div className="text-2xl font-bold">Github AI Application Evaluation</div>
        <Button variant="default" onClick={() => router.push("/tool")}>
          Get Started
        </Button>
      </div>
      <Footer />
    </div>
  )
}
