import Link from "next/link";
import { LogIn, LogOut } from "lucide-react";

import { Button } from "@/components/ui/button";

export default function GuestPage() {
  return (
    <div className="flex min-h-screen flex-col items-center justify-center bg-background p-4">
      <main className="container flex max-w-3xl flex-col items-center justify-center gap-12 py-8 md:py-16 lg:py-24 text-center">
        <div className="space-y-4">
          <h1 className="text-5xl font-bold tracking-tight sm:text-6xl">
            Guest Portal
          </h1>
          <p className="text-2xl text-muted-foreground">
            Please select whether you want to check in or check out.
          </p>
        </div>

        <div className="grid w-full max-w-md gap-8 sm:grid-cols-1 md:max-w-2xl md:grid-cols-2">
          <Link href="/guest/check-in/" className="w-full">
            <Button
              variant="outline"
              className="h-48 w-full flex-col gap-6 p-8 shadow-sm transition-all hover:bg-primary hover:text-primary-foreground"
            >
              <LogIn style={{ height: "64px", width: "64px" }} />
              <span className="text-2xl font-medium">Check In</span>
            </Button>
          </Link>

          <Link href="/guest/check-out/search" className="w-full">
            <Button
              variant="outline"
              className="h-48 w-full flex-col gap-6 p-8 shadow-sm transition-all hover:bg-primary hover:text-primary-foreground"
            >
              <LogOut style={{ height: "64px", width: "64px" }} />
              <span className="text-2xl font-medium">Check Out</span>
            </Button>
          </Link>
        </div>

        <div className="mt-8">
          <Link href="/">
            <Button variant="ghost" className="text-muted-foreground">
              Back to Home
            </Button>
          </Link>
        </div>
      </main>

      <footer className="mt-auto py-6 text-center text-sm text-muted-foreground">
        © {new Date().getFullYear()} Youth Mentorship Program. All rights
        reserved.
      </footer>
    </div>
  );
}
