"use client";

import * as React from "react";
import { X } from "lucide-react";
import { cn } from "@/lib/utils";

interface DialogContextType {
  open: boolean;
  onOpenChange: (open: boolean) => void;
}

const DialogContext = React.createContext<DialogContextType | undefined>(undefined);

interface DialogProps {
  open?: boolean;
  onOpenChange?: (open: boolean) => void;
  children: React.ReactNode;
}

const Dialog = ({ open = false, onOpenChange, children }: DialogProps) => {
  return (
    <DialogContext.Provider value={{ open, onOpenChange: onOpenChange || (() => {}) }}>
      {children}
    </DialogContext.Provider>
  );
};

interface DialogTriggerProps extends React.HTMLAttributes<HTMLDivElement> {
  asChild?: boolean;
}

const DialogTrigger = ({ className, children, asChild = false, ...props }: DialogTriggerProps) => {
  const context = React.useContext(DialogContext);
  
  if (asChild && React.isValidElement(children)) {
    return React.cloneElement(children as React.ReactElement<any>, {
      onClick: (e: React.MouseEvent) => {
        context?.onOpenChange(true);
        (children.props as any)?.onClick?.(e);
      }
    });
  }

  return (
    <div
      className={cn("cursor-pointer", className)}
      onClick={() => context?.onOpenChange(true)}
      {...props}
    >
      {children}
    </div>
  );
};

const DialogContent = React.forwardRef<
  HTMLDivElement,
  React.HTMLAttributes<HTMLDivElement>
>(({ className, children, ...props }, ref) => {
  const context = React.useContext(DialogContext);

  if (!context?.open) return null;

  return (
    <>
      {/* Backdrop */}
      <div 
        className="fixed inset-0 z-50 bg-black/60 backdrop-blur-md animate-in fade-in-0 duration-300"
        onClick={() => context.onOpenChange(false)}
      />
      
      {/* Dialog */}
      <div className="fixed inset-0 z-50 flex items-start justify-center p-4 pt-6 pb-8">
        <div
          ref={ref}
          className={cn(
            "relative w-full bg-background border rounded-xl shadow-2xl",
            "animate-in fade-in-0 zoom-in-95 duration-300 slide-in-from-bottom-4",
            "border-border/50 backdrop-blur-sm",
            className
          )}
          onClick={(e) => e.stopPropagation()}
          {...props}
        >
          <button
            className="absolute right-6 top-6 rounded-full p-2 opacity-70 ring-offset-background transition-all hover:opacity-100 hover:bg-muted focus:outline-none focus:ring-2 focus:ring-ring focus:ring-offset-2"
            onClick={() => context.onOpenChange(false)}
          >
            <X className="h-4 w-4" />
            <span className="sr-only">Close</span>
          </button>
          {children}
        </div>
      </div>
    </>
  );
});

DialogContent.displayName = "DialogContent";

const DialogHeader = ({
  className,
  ...props
}: React.HTMLAttributes<HTMLDivElement>) => (
  <div
    className={cn(
      "flex flex-col space-y-1.5 text-center sm:text-left p-6 pb-0",
      className
    )}
    {...props}
  />
);

const DialogTitle = React.forwardRef<
  HTMLHeadingElement,
  React.HTMLAttributes<HTMLHeadingElement>
>(({ className, ...props }, ref) => (
  <h3
    ref={ref}
    className={cn(
      "text-lg font-semibold leading-none tracking-tight",
      className
    )}
    {...props}
  />
));

DialogTitle.displayName = "DialogTitle";

const DialogDescription = React.forwardRef<
  HTMLParagraphElement,
  React.HTMLAttributes<HTMLParagraphElement>
>(({ className, ...props }, ref) => (
  <p
    ref={ref}
    className={cn("text-sm text-muted-foreground", className)}
    {...props}
  />
));

DialogDescription.displayName = "DialogDescription";

export {
  Dialog,
  DialogTrigger,
  DialogContent,
  DialogHeader,
  DialogTitle,
  DialogDescription,
}; 