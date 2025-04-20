"use client";

import { useId, useState, useEffect } from "react";
import { ClockIcon } from "lucide-react";
import { Input } from "@/components/ui/input";

interface TimePickerProps {
  value: string; // ISO string or time string depending on your use
  onChange: (value: string) => void;
}

export default function TimePicker({ value, onChange }: TimePickerProps) {
  const id = useId();

  // Extract time from ISO or use as-is
  const [time, setTime] = useState<string>(() => {
    try {
      const parsed = new Date(value);
      return parsed.toTimeString().slice(0, 8); // "HH:mm:ss"
    } catch {
      return "12:00:00";
    }
  });

  useEffect(() => {
    // Return only the time part as "HH:mm:ss"
    onChange(time);
  }, [time]);

  return (
    <div>
      {/* <Label htmlFor={id} className="text-sm font-medium mb-2 block">
        Select Time
      </Label> */}
      <div className="relative">
        <Input
          id={id}
          type="time"
          step="1"
          value={time}
          onChange={(e) => setTime(e.target.value)}
          className="peer appearance-none ps-9 [&::-webkit-calendar-picker-indicator]:hidden [&::-webkit-calendar-picker-indicator]:appearance-none"
        />
        <div className="text-muted-foreground/80 pointer-events-none absolute inset-y-0 start-0 flex items-center justify-center ps-3 peer-disabled:opacity-50">
          <ClockIcon size={16} aria-hidden="true" />
        </div>
      </div>
    </div>
  );
}
