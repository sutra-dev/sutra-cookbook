"use client";

import { useState, useEffect } from "react";
import { CheckCircle, XCircle, AlertCircle, Info, X } from "lucide-react";
import { cn } from "@/lib/utils";

export type ToastType = "success" | "error" | "warning" | "info";

interface Toast {
  id: string;
  type: ToastType;
  title: string;
  description?: string;
  duration?: number;
}

interface ToastProps extends Toast {
  onRemove: (id: string) => void;
}

const ToastComponent = ({ id, type, title, description, duration = 4000, onRemove }: ToastProps) => {
  useEffect(() => {
    const timer = setTimeout(() => {
      onRemove(id);
    }, duration);

    return () => clearTimeout(timer);
  }, [id, duration, onRemove]);

  const icons = {
    success: CheckCircle,
    error: XCircle,
    warning: AlertCircle,
    info: Info,
  };

  const Icon = icons[type];

  const styles = {
    success: "bg-green-50 border-green-200 text-green-800 shadow-green-100",
    error: "bg-red-50 border-red-200 text-red-800 shadow-red-100",
    warning: "bg-yellow-50 border-yellow-200 text-yellow-800 shadow-yellow-100",
    info: "bg-blue-50 border-blue-200 text-blue-800 shadow-blue-100",
  };

  return (
    <div
      className={cn(
        "flex items-start gap-3 p-4 border rounded-xl shadow-lg max-w-sm w-full backdrop-blur-sm",
        "animate-in slide-in-from-right-2 duration-300",
        styles[type]
      )}
    >
      <Icon className="h-5 w-5 mt-0.5 flex-shrink-0" />
      <div className="flex-1 min-w-0">
        <p className="font-medium text-sm">{title}</p>
        {description && (
          <p className="text-sm opacity-90 mt-1">{description}</p>
        )}
      </div>
      <button
        onClick={() => onRemove(id)}
        className="flex-shrink-0 opacity-70 hover:opacity-100 transition-opacity"
      >
        <X className="h-4 w-4" />
      </button>
    </div>
  );
};

// Toast container and hook
let toastCount = 0;

export const useToast = () => {
  const [toasts, setToasts] = useState<Toast[]>([]);

  const addToast = (toast: Omit<Toast, "id">) => {
    const id = `toast-${++toastCount}`;
    setToasts(prev => [...prev, { ...toast, id }]);
    return id;
  };

  const removeToast = (id: string) => {
    setToasts(prev => prev.filter(toast => toast.id !== id));
  };

  const ToastContainer = () => (
    <div className="fixed top-4 right-4 z-[100] flex flex-col gap-2">
      {toasts.map(toast => (
        <ToastComponent
          key={toast.id}
          {...toast}
          onRemove={removeToast}
        />
      ))}
    </div>
  );

  return {
    addToast,
    removeToast,
    ToastContainer,
  };
}; 