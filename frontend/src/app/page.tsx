import Image from "next/image";
import Header from '@/components/layout/Header'
import Footer from '@/components/layout/Footer'
import { Button } from "antd";

export default function Home() {
  return (
    <div className="font-sans grid grid-rows-[20px_1fr_20px] items-center justify-items-center min-h-screen p-8 pb-20 gap-16 sm:p-20">
      <Header />
<div className="text-center space-y-8">
  <div>Github AI Application Evaluation</div>
  <Button type="primary">Get Started</Button>
</div>
      <Footer />
    </div>
  );
}
