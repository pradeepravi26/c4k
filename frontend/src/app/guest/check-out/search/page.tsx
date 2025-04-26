"use client";

import { useEffect, useState } from "react";
import Link from "next/link";
import { Search, ArrowLeft } from "lucide-react";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";

interface Guest {
  id: string;
  full_name: string;
  role: string;
  is_active: boolean;
}

export default function GuestCheckOutSearch() {
  const [searchTerm, setSearchTerm] = useState("");
  const [allGuests, setAllGuests] = useState<Guest[]>([]);
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    const fetchGuests = async () => {
      setLoading(true);
      try {
        const res = await fetch(
          `${process.env.FASTAPI_BASE_URL}/guests/check-out`
        );
        if (!res.ok) throw new Error("Failed to fetch guests for checkout");

        const data = await res.json();

        if (Array.isArray(data)) {
          setAllGuests(data);
        } else {
          console.error("Invalid response format", data);
          setAllGuests([]);
        }
      } catch (error) {
        console.error("Error fetching checkout guests", error);
        setAllGuests([]);
      } finally {
        setLoading(false);
      }
    };

    fetchGuests();
  }, []);

  const filteredGuests = allGuests.filter((guest: Guest) => {
    const search = searchTerm.toLowerCase();
    return guest.full_name.toLowerCase().includes(search);
  });

  return (
    <div className="flex min-h-screen flex-col bg-background p-4">
      <div className="container max-w-4xl mx-auto py-8">
        <div className="flex items-center mb-8">
          <Link href="/guest">
            <Button variant="ghost" size="icon" className="mr-2">
              <ArrowLeft className="h-5 w-5" />
            </Button>
          </Link>
          <h1 className="text-3xl font-bold">Guest Check-Out</h1>
        </div>

        {/* Search bar */}
        <div className="relative mb-8">
          <Search className="absolute left-3 top-1/2 h-5 w-5 -translate-y-1/2 text-muted-foreground" />
          <Input
            type="text"
            placeholder="Search guests..."
            className="pl-10 w-full"
            value={searchTerm}
            onChange={(e) => setSearchTerm(e.target.value)}
          />
        </div>

        <p className="text-sm text-muted-foreground mb-4">
          {loading
            ? "Loading..."
            : `${filteredGuests.length} guest(s) available for check-out`}
        </p>

        {/* Grid of guest names */}
        {filteredGuests.length > 0 ? (
          <div className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 gap-4">
            {filteredGuests.map((guest: Guest) => (
              <Link
                key={guest.id}
                href={`/guest/check-out/${guest.id}`}
                className="w-full"
              >
                <Button
                  variant="outline"
                  className="w-full h-20 text-lg justify-start px-4 hover:bg-primary hover:text-primary-foreground"
                >
                  <div className="flex flex-col items-start">
                    <span className="text-lg font-medium">
                      {guest.full_name || "Unnamed"}
                    </span>
                  </div>
                </Button>
              </Link>
            ))}
          </div>
        ) : (
          !loading && (
            <div className="text-center py-12">
              <p className="text-xl text-muted-foreground">
                No guests available for check-out
              </p>
              <p className="text-sm text-muted-foreground mt-2">
                Try a different search term
              </p>
            </div>
          )
        )}
      </div>

      <footer className="mt-auto py-6 text-center text-sm text-muted-foreground">
        © {new Date().getFullYear()} Youth Mentorship Program. All rights
        reserved.
      </footer>
    </div>
  );
}
