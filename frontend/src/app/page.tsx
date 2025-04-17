import Link from "next/link";
import { UserRound, Users, UserPlus } from "lucide-react";

import { Button } from "@/components/ui/button";

export default function CheckInPage() {
  return (
    <div className="flex min-h-screen flex-col items-center justify-center bg-background p-4">
      <main className="container flex max-w-3xl flex-col items-center justify-center gap-12 py-8 md:py-16 lg:py-24 text-center">
        <div className="space-y-4">
          <h1 className="text-5xl font-bold tracking-tight sm:text-6xl">C4K</h1>
          <p className="text-2xl text-muted-foreground">
            Welcome! Please select your role to check in.
          </p>
        </div>

        <div className="grid w-full max-w-md gap-8 sm:grid-cols-1 md:max-w-3xl md:grid-cols-3">
          <Link href="/student" className="w-full">
            <Button
              variant="outline"
              className="h-48 w-full flex-col gap-6 p-8 shadow-sm transition-all hover:bg-primary hover:text-primary-foreground"
            >
              <UserRound className="!h-16 !w-16" />
              {/* <UserRound style={{ height: "64px", width: "64px" }} /> */}
              <span className="text-2xl font-medium">Student</span>
            </Button>
          </Link>

          <Link href="/volunteer" className="w-full">
            <Button
              variant="outline"
              className="h-48 w-full flex-col gap-6 p-8 shadow-sm transition-all hover:bg-primary hover:text-primary-foreground"
            >
              <Users className="!h-16 !w-16" />
              {/* <Users style={{ height: "64px", width: "64px" }} /> */}
              <span className="text-2xl font-medium">Volunteer</span>
            </Button>
          </Link>

          <Link href="/guest" className="w-full">
            <Button
              variant="outline"
              className="h-48 w-full flex-col gap-6 p-8 shadow-sm transition-all hover:bg-primary hover:text-primary-foreground"
            >
              <UserPlus className="!h-16 !w-16" />
              {/* <UserPlus style={{ height: "64px", width: "64px" }} /> */}
              <span className="text-2xl font-medium">Guest</span>
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
