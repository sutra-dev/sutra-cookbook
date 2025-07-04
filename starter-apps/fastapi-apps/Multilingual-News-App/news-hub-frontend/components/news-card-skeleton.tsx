import { Card, CardContent, CardFooter, CardHeader } from "@/components/ui/card";

export function NewsCardSkeleton() {
  return (
    <Card className="overflow-hidden">
      {/* Image skeleton */}
      <div className="h-48 w-full skeleton" />
      
      <CardHeader className="space-y-2">
        {/* Source and date skeleton */}
        <div className="flex items-center justify-between">
          <div className="h-4 w-20 skeleton rounded" />
          <div className="h-4 w-24 skeleton rounded" />
        </div>
        {/* Title skeleton */}
        <div className="space-y-2">
          <div className="h-5 w-full skeleton rounded" />
          <div className="h-5 w-3/4 skeleton rounded" />
        </div>
      </CardHeader>
      
      <CardContent>
        {/* Description skeleton */}
        <div className="space-y-2">
          <div className="h-4 w-full skeleton rounded" />
          <div className="h-4 w-full skeleton rounded" />
          <div className="h-4 w-2/3 skeleton rounded" />
        </div>
      </CardContent>
      
      <CardFooter>
        {/* Button skeleton */}
        <div className="h-9 w-full skeleton rounded-lg" />
      </CardFooter>
    </Card>
  );
} 