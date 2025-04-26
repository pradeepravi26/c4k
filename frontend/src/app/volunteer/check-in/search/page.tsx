"use client";

import { useEffect, useState } from "react";
import Link from "next/link";
import { Search, ArrowLeft } from "lucide-react";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";

interface Volunteer {
  id: string;
  full_name: string;
  preferred_name: string | null;
  c4k_id: string;
  role: string;
  is_active: boolean;
}

export default function VolunteerCheckInSearch() {
  const [searchTerm, setSearchTerm] = useState("");
  const [allVolunteers, setAllVolunteers] = useState<Volunteer[]>([]);
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    const fetchVolunteers = async () => {
      setLoading(true);
      try {
        const res = await fetch(
          `${process.env.FASTAPI_BASE_URL}/users/check-in?role=volunteer`
        );
        const data = await res.json();

        if (Array.isArray(data)) {
          setAllVolunteers(data);
        } else {
          console.error("Invalid response format", data);
          setAllVolunteers([]);
        }
      } catch (error) {
        console.error("Failed to fetch volunteers", error);
        setAllVolunteers([]);
      } finally {
        setLoading(false);
      }
    };

    fetchVolunteers();
  }, []);

  const filteredVolunteers = allVolunteers.filter((volunteer: Volunteer) => {
    const search = searchTerm.toLowerCase();
    return (
      (volunteer.full_name &&
        volunteer.full_name.toLowerCase().includes(search)) ||
      (volunteer.preferred_name &&
        volunteer.preferred_name.toLowerCase().includes(search)) ||
      (volunteer.c4k_id && volunteer.c4k_id.toLowerCase().includes(search))
    );
  });

  return (
    <div className="flex min-h-screen flex-col bg-background p-4">
      <div className="container max-w-4xl mx-auto py-8">
        <div className="flex items-center mb-8">
          <Link href="/volunteer">
            <Button variant="ghost" size="icon" className="mr-2">
              <ArrowLeft className="h-5 w-5" />
            </Button>
          </Link>
          <h1 className="text-3xl font-bold">Volunteer Check-In</h1>
        </div>

        {/* Search bar */}
        <div className="relative mb-8">
          <Search className="absolute left-3 top-1/2 h-5 w-5 -translate-y-1/2 text-muted-foreground" />
          <Input
            type="text"
            placeholder="Search volunteers..."
            className="pl-10 w-full"
            value={searchTerm}
            onChange={(e) => setSearchTerm(e.target.value)}
          />
        </div>

        <p className="text-sm text-muted-foreground mb-4">
          {loading
            ? "Loading..."
            : `${filteredVolunteers.length} volunteer(s) available for check-in`}
        </p>

        {/* Grid of volunteer names */}
        {filteredVolunteers.length > 0 ? (
          <div className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 gap-4">
            {filteredVolunteers.map((volunteer: Volunteer) => (
              <Link
                key={volunteer.id}
                href={`/volunteer/check-in/${volunteer.id}`}
                className="w-full"
              >
                <Button
                  variant="outline"
                  className="w-full h-20 text-lg justify-start px-4 hover:bg-primary hover:text-primary-foreground"
                >
                  <div className="flex flex-col items-start">
                    <span className="text-lg font-medium">
                      {volunteer.preferred_name ||
                        volunteer.full_name ||
                        "Unnamed"}
                    </span>
                    <span className="text-sm text-muted-foreground">
                      {volunteer.c4k_id || "N/A"} &middot;{" "}
                      {volunteer.full_name || "N/A"}
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
                No volunteers available for check-in
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
