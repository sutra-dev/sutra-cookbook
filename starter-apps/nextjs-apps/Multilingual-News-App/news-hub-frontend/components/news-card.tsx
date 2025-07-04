"use client";

import React from "react";
import Image from "next/image";
import { Card, CardContent, CardFooter, CardHeader } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Calendar, ExternalLink, Share2, Clock } from "lucide-react";
import { NewsItem } from "@/lib/api";
import { cn } from "@/lib/utils";

interface NewsCardProps {
  news: NewsItem;
  className?: string;
}

export function NewsCard({ news, className }: NewsCardProps) {
  const handleShare = async () => {
    if (navigator.share) {
      try {
        await navigator.share({
          title: news.title,
          text: news.snippet,
          url: news.link,
        });
      } catch (error) {
        console.error("Error sharing:", error);
      }
    }
  };

  const formatDate = (dateString?: string) => {
    if (!dateString) return "Recent";
    try {
      const date = new Date(dateString);
      const now = new Date();
      const diffTime = Math.abs(now.getTime() - date.getTime());
      const diffDays = Math.ceil(diffTime / (1000 * 60 * 60 * 24));
      
      if (diffDays === 1) return "Yesterday";
      if (diffDays < 7) return `${diffDays} days ago`;
      
      return date.toLocaleDateString("en-US", {
        month: "short",
        day: "numeric",
        year: "numeric",
      });
    } catch {
      return dateString;
    }
  };

  // Enhanced description processing
  const getEnhancedDescription = (snippet: string) => {
    // Clean up the snippet and provide more context
    let description = snippet;
    
    // Remove redundant source information if it appears in the snippet
    description = description.replace(new RegExp(`${news.source}[\\s-]*`, 'gi'), '');
    
    // Add more context if the snippet is too short
    if (description.length < 100 && description.length > 0) {
      description = `${description} This developing story covers important updates in the field. Click to read the full article for comprehensive details and analysis.`;
    }
    
    return description;
  };

  const enhancedDescription = getEnhancedDescription(news.snippet);
  const readingTime = Math.max(1, Math.ceil(enhancedDescription.split(' ').length / 200));

  return (
    <Card className={cn("news-card overflow-hidden group border-0 shadow-md hover:shadow-xl transition-all duration-300", className)}>
      {news.imageUrl && (
        <div className="relative h-52 w-full overflow-hidden">
          <Image
            src={news.imageUrl}
            alt={news.title}
            fill
            className="object-cover transition-transform duration-500 group-hover:scale-110"
            sizes="(max-width: 768px) 100vw, (max-width: 1200px) 50vw, 33vw"
          />
          <div className="absolute inset-0 bg-gradient-to-t from-black/40 via-black/10 to-transparent" />
          <div className="absolute top-4 right-4 bg-black/70 backdrop-blur-sm text-white px-3 py-1 rounded-full text-xs font-medium">
            {readingTime} min read
          </div>
        </div>
      )}
      
      <CardHeader className="space-y-3 pb-4">
        <div className="flex items-center justify-between text-sm">
          <div className="flex items-center gap-2">
            <span className="font-semibold text-primary bg-primary/10 px-2 py-1 rounded-md text-xs">
              {news.source}
            </span>
          </div>
          <div className="flex items-center gap-1 text-muted-foreground">
            <Clock className="h-3 w-3" />
            <span className="text-xs">{formatDate(news.date)}</span>
          </div>
        </div>
        <h3 className="text-xl font-bold leading-tight line-clamp-3 group-hover:text-primary transition-colors duration-200">
          {news.title}
        </h3>
      </CardHeader>
      
      <CardContent className="pb-6">
        <div className="space-y-3">
          <p className="text-muted-foreground leading-relaxed line-clamp-5 text-sm">
            {enhancedDescription}
          </p>
          
          {/* Article highlights */}
          <div className="flex flex-wrap gap-2">
            {news.snippet.toLowerCase().includes('technology') && (
              <span className="bg-blue-100 text-blue-800 text-xs px-2 py-1 rounded-full">Tech</span>
            )}
            {news.snippet.toLowerCase().includes('business') && (
              <span className="bg-green-100 text-green-800 text-xs px-2 py-1 rounded-full">Business</span>
            )}
            {news.snippet.toLowerCase().includes('singapore') && (
              <span className="bg-purple-100 text-purple-800 text-xs px-2 py-1 rounded-full">Singapore</span>
            )}
            {(news.snippet.toLowerCase().includes('new') || news.snippet.toLowerCase().includes('launch')) && (
              <span className="bg-orange-100 text-orange-800 text-xs px-2 py-1 rounded-full">Breaking</span>
            )}
          </div>
        </div>
      </CardContent>
      
      <CardFooter className="flex justify-between gap-2 pt-0">
        <Button
          variant="default"
          size="sm"
          className="flex-1 bg-gradient-to-r from-primary to-primary/80 hover:from-primary/90 hover:to-primary/70 transition-all duration-200"
          asChild
        >
          <a href={news.link} target="_blank" rel="noopener noreferrer">
            Read Full Story
            <ExternalLink className="ml-2 h-3 w-3" />
          </a>
        </Button>
        <Button
          variant="outline"
          size="icon"
          onClick={handleShare}
          className="opacity-70 hover:opacity-100 transition-opacity border-primary/20 hover:border-primary/40"
          title="Share this article"
        >
          <Share2 className="h-4 w-4" />
        </Button>
      </CardFooter>
    </Card>
  );
} 