import { User } from "lucide-react";

interface GreetingSectionProps {
  userName?: string;
  pendingTasksCount: number;
}

export function GreetingSection({ userName = "User", pendingTasksCount }: GreetingSectionProps) {
  const hours = new Date().getHours();
  const greeting =
    hours < 12 ? "Good Morning" : hours < 18 ? "Good Afternoon" : "Good Evening";

  return (
    <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4">
      <div>
        <h1 className="text-3xl font-bold tracking-tight text-slate-900">
          {greeting}, {userName}.
        </h1>
        <p className="text-slate-500 mt-1">
          {pendingTasksCount > 0 ? (
            <>
              You have <span className="font-semibold text-indigo-600">{pendingTasksCount} tasks</span> pending today.
            </>
          ) : (
             "You're all caught up for today!"
          )}
        </p>
      </div>
    </div>
  );
}
