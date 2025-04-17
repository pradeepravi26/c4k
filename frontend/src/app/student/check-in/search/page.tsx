"use client";

import { useEffect, useState } from "react";
import Link from "next/link";
import { Search, ArrowLeft } from "lucide-react";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";

export default function StudentCheckInSearch() {
  const [searchTerm, setSearchTerm] = useState("");
  const [allStudents, setAllStudents] = useState([]);
  const [loading, setLoading] = useState(false);

  // Fetch all users with role=student
  useEffect(() => {
    const fetchStudents = async () => {
      setLoading(true);
      try {
        const res = await fetch("http://localhost:8000/users?role=student");
        const data = await res.json();
        setAllStudents(data);
      } catch (error) {
        console.error("Failed to fetch students", error);
        setAllStudents([]);
      } finally {
        setLoading(false);
      }
    };

    fetchStudents();
  }, []);

  // Filter on the frontend
  const filteredStudents = allStudents.filter((student: any) =>
    student.full_name.toLowerCase().includes(searchTerm.toLowerCase())
  );

  return (
    <div className="flex min-h-screen flex-col bg-background p-4">
      <div className="container max-w-4xl mx-auto py-8">
        <div className="flex items-center mb-8">
          <Link href="/student">
            <Button variant="ghost" size="icon" className="mr-2">
              <ArrowLeft className="h-5 w-5" />
            </Button>
          </Link>
          <h1 className="text-3xl font-bold">Student Check-In</h1>
        </div>

        {/* Search bar */}
        <div className="relative mb-8">
          <Search className="absolute left-3 top-1/2 h-5 w-5 -translate-y-1/2 text-muted-foreground" />
          <Input
            type="text"
            placeholder="Search students..."
            className="pl-10 w-full"
            value={searchTerm}
            onChange={(e) => setSearchTerm(e.target.value)}
          />
        </div>

        <p className="text-sm text-muted-foreground mb-4">
          {loading
            ? "Loading..."
            : `${filteredStudents.length} student(s) found`}
        </p>

        {/* Grid of student names */}
        {filteredStudents.length > 0 ? (
          <div className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 gap-4">
            {filteredStudents.map((student: any) => (
              <Link
                key={student.id}
                href={`/student/check-in/${student.id}`}
                className="w-full"
              >
                <Button
                  variant="outline"
                  className="w-full h-20 text-lg justify-start px-4 hover:bg-primary hover:text-primary-foreground"
                >
                  <div className="flex flex-col items-start">
                    <span className="text-lg font-medium">
                      {student.preferred_name || student.full_name}
                    </span>
                    <span className="text-sm text-muted-foreground">
                      {student.c4k_id} &middot; {student.full_name}
                    </span>
                  </div>
                </Button>
              </Link>
            ))}
          </div>
        ) : (
          !loading && (
            <div className="text-center py-12">
              <p className="text-xl text-muted-foreground">No students found</p>
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
