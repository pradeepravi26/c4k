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
import { format } from "date-fns";

interface Guest {
  id: string;
  full_name: string;
  role: string;
  is_active: boolean;
}

export default function GuestCheckOut({
  params,
}: {
  params: Promise<{ id: string }>;
}) {
  const router = useRouter();
  const [guest, setGuest] = useState<Guest | null>(null);
  const [checkOutTime] = useState<string>(
    format(new Date(), "yyyy-MM-dd'T'HH:mm")
  );
  const [loading, setLoading] = useState(true);
  const [submitting, setSubmitting] = useState(false);
  const [status, setStatus] = useState<"idle" | "success" | "error">("idle");
  const [errorMessage, setErrorMessage] = useState("");
  const [dialogOpen, setDialogOpen] = useState(false);
  const [resolvedParams, setResolvedParams] = useState<{ id: string } | null>(
    null
  );

  useEffect(() => {
    (async () => {
      const resolved = await params;
      setResolvedParams(resolved);
    })();
  }, [params]);

  useEffect(() => {
    if (!resolvedParams) return;

    (async () => {
      try {
        const res = await fetch(
          `${process.env.FASTAPI_BASE_URL}/users/${resolvedParams.id}`
        );
        if (!res.ok) throw new Error("Failed to fetch guest");
        const data: Guest = await res.json();
        setGuest(data);
      } catch (err) {
        console.error(err);
      } finally {
        setLoading(false);
      }
    })();
  }, [resolvedParams]);

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
      if (!resolvedParams) throw new Error("Invalid parameters");

      const isoTime = new Date(checkOutTime).toISOString();
      const checkOutRes = await fetch(
        `${process.env.FASTAPI_BASE_URL}/guests/check-out/${
          resolvedParams.id
        }?check_out_time=${encodeURIComponent(isoTime)}`,
        {
          method: "POST",
        }
      );

      if (!checkOutRes.ok) {
        const errorData = await checkOutRes.json();
        throw new Error(errorData.detail || "Check-out failed");
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

  if (loading || !resolvedParams) {
    return (
      <div className="flex min-h-screen flex-col items-center justify-center bg-background p-4">
        <p className="text-lg">Loading guest information...</p>
      </div>
    );
  }

  return (
    <div className="flex min-h-screen flex-col bg-background p-4">
      <div className="container max-w-md mx-auto py-8">
        <div className="flex items-center mb-8">
          <Link href="/guest/check-out/search">
            <Button variant="ghost" size="icon" className="mr-2">
              <ArrowLeft className="h-5 w-5" />
            </Button>
          </Link>
          <h1 className="text-3xl font-bold">Guest Check-Out</h1>
        </div>

        <Card>
          <CardHeader>
            <CardTitle>{guest?.full_name || "Guest"}</CardTitle>
          </CardHeader>

          <form onSubmit={handleSubmit}>
            <CardContent>
              <p className="text-muted-foreground">
                Press the button below to check out this guest.
              </p>
            </CardContent>
            <div className="my-4"></div>
            <CardFooter>
              <Button type="submit" className="w-full" disabled={submitting}>
                {submitting ? "Checking out..." : "Check Out"}
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
                  ? "Guest has been successfully checked out. Redirecting to home page in 5 seconds."
                  : errorMessage ||
                    "There was an error checking out. Please try again."}
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
