import { Card, CardContent, CardHeader } from "@/components/ui/card";

export function DashboardSkeleton() {
  return (
    <div className="space-y-8 animate-pulse">
      {/* Greeting Skeleton */}
      <div className="space-y-2">
        <div className="h-8 w-64 bg-slate-200 rounded"></div>
        <div className="h-5 w-48 bg-slate-200 rounded"></div>
      </div>

      {/* Projects Grid Skeleton */}
      <div className="space-y-4">
        <div className="h-6 w-32 bg-slate-200 rounded"></div>
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          {[1, 2, 3].map((i) => (
            <Card key={i} className="border-white/40 bg-white/40">
              <CardHeader className="pb-2">
                <div className="h-5 w-1/2 bg-slate-200 rounded mb-2"></div>
                <div className="h-4 w-3/4 bg-slate-200 rounded"></div>
              </CardHeader>
              <CardContent>
                <div className="h-2 w-full bg-slate-200 rounded-full mt-4"></div>
                <div className="flex justify-between mt-2">
                   <div className="h-3 w-10 bg-slate-200 rounded"></div>
                   <div className="h-3 w-10 bg-slate-200 rounded"></div>
                </div>
              </CardContent>
            </Card>
          ))}
        </div>
      </div>

      {/* Tasks Skeleton */}
      <div className="space-y-4">
         <div className="h-6 w-32 bg-slate-200 rounded"></div>
         <div className="space-y-3">
            {[1, 2, 3, 4].map((i) => (
                <div key={i} className="h-12 w-full bg-slate-200 rounded-lg"></div>
            ))}
         </div>
      </div>
    </div>
  );
}
