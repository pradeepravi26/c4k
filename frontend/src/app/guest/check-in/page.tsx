"use client";

import React, { useEffect, useState } from "react";
import { useRouter } from "next/navigation";
import Link from "next/link";
import { ArrowLeft, Home } from "lucide-react";
import { Button } from "@/components/ui/button";
import {
  Card,
  CardContent,
  CardFooter,
  CardHeader,
  CardTitle,
} from "@/components/ui/card";
import {
  Dialog,
  DialogContent,
  DialogDescription,
  DialogFooter,
  DialogHeader,
  DialogTitle,
} from "@/components/ui/dialog";
import { Input } from "@/components/ui/input";

export default function GuestCheckIn() {
  const router = useRouter();
  const [guestName, setGuestName] = useState("");
  const [submitting, setSubmitting] = useState(false);
  const [status, setStatus] = useState<"idle" | "success" | "error">("idle");
  const [errorMessage, setErrorMessage] = useState("");
  const [dialogOpen, setDialogOpen] = useState(false);

  useEffect(() => {
    if (status !== "idle") {
      setDialogOpen(true);

      if (status === "success") {
        const timer = setTimeout(() => {
          router.push("/");
        }, 5000);
        return () => clearTimeout(timer);
      }
    }
  }, [status, router]);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setSubmitting(true);

    try {
      if (!guestName.trim()) throw new Error("Please enter your full name");

      const res = await fetch("http://localhost:8000/guests/check-in", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ full_name: guestName.trim() }),
      });

      if (!res.ok) {
        const errorData = await res.json();
        throw new Error(errorData.detail || "Check-in failed");
      }

      setStatus("success");
    } catch (err) {
      console.error(err);
      setErrorMessage(err instanceof Error ? err.message : "Unknown error");
      setStatus("error");
    } finally {
      setSubmitting(false);
    }
  };

  return (
    <div className="flex min-h-screen flex-col bg-background p-4">
      <div className="container max-w-md mx-auto py-8">
        <div className="flex items-center mb-8">
          <Link href="/guest">
            <Button variant="ghost" size="icon" className="mr-2">
              <ArrowLeft className="h-5 w-5" />
            </Button>
          </Link>
          <h1 className="text-3xl font-bold">Guest Check-In</h1>
        </div>

        <Card>
          <form onSubmit={handleSubmit}>
            <CardHeader>
              <CardTitle>Enter Your Full Name</CardTitle>
            </CardHeader>
            <CardContent>
              <Input
                type="text"
                placeholder="Full Name"
                value={guestName}
                onChange={(e) => setGuestName(e.target.value)}
                required
              />
            </CardContent>
            <div className="my-4"></div>
            <CardFooter>
              <Button type="submit" className="w-full" disabled={submitting}>
                {submitting ? "Checking in..." : "Check In"}
              </Button>
            </CardFooter>
          </form>
        </Card>

        <Dialog open={dialogOpen} onOpenChange={setDialogOpen}>
          <DialogContent>
            <DialogHeader>
              <DialogTitle>
                {status === "success" ? "Success!" : "Error"}
              </DialogTitle>
              <DialogDescription>
                {status === "success"
                  ? "Guest has been successfully checked in. Redirecting to home page in 5 seconds."
                  : errorMessage ||
                    "There was an error checking in. Please try again."}
              </DialogDescription>
            </DialogHeader>
            <DialogFooter>
              {status === "success" ? (
                <Button
                  onClick={() => router.push("/")}
                  className="w-full flex items-center justify-center"
                >
                  <Home className="mr-2 h-4 w-4" /> Go to Home
                </Button>
              ) : (
                <Button
                  variant="outline"
                  className="w-full"
                  onClick={() => {
                    setDialogOpen(false);
                    setStatus("idle");
                  }}
                >
                  Try Again
                </Button>
              )}
            </DialogFooter>
          </DialogContent>
        </Dialog>
      </div>

      <footer className="mt-auto py-6 text-center text-sm text-muted-foreground">
        © {new Date().getFullYear()} Youth Mentorship Program. All rights
        reserved.
      </footer>
    </div>
  );
}
