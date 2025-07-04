"use client";

import { useState } from "react";
import { Settings, Eye, EyeOff, Save, RotateCcw, ExternalLink, Key, Globe } from "lucide-react";
import { Button } from "@/components/ui/button";
import {
  Dialog,
  DialogContent,
  DialogDescription,
  DialogHeader,
  DialogTitle,
  DialogTrigger,
} from "@/components/ui/dialog";
import { useApiKeys } from "@/lib/hooks/use-api-keys";
import { useToast } from "@/components/ui/toast";

export function SettingsDialog() {
  const { apiKeys, updateApiKeys, clearApiKeys } = useApiKeys();
  const { addToast, ToastContainer } = useToast();
  const [isOpen, setIsOpen] = useState(false);
  const [showSerperKey, setShowSerperKey] = useState(false);
  const [showSutraKey, setShowSutraKey] = useState(false);
  const [localKeys, setLocalKeys] = useState({
    serperApiKey: '',
    sutraApiKey: '',
  });

  // Initialize local keys when dialog opens
  const handleOpenChange = (open: boolean) => {
    setIsOpen(open);
    if (open) {
      setLocalKeys({
        serperApiKey: apiKeys.serperApiKey,
        sutraApiKey: apiKeys.sutraApiKey,
      });
    }
  };

  const handleSave = () => {
    updateApiKeys(localKeys);
    setIsOpen(false);
    addToast({
      type: "success",
      title: "Settings saved",
      description: "Your API keys have been saved successfully."
    });
  };

  const handleReset = () => {
    clearApiKeys();
    setLocalKeys({ serperApiKey: '', sutraApiKey: '' });
    addToast({
      type: "info",
      title: "Settings reset",
      description: "Your API keys have been cleared."
    });
  };

  return (
    <>
      <ToastContainer />
      <Dialog open={isOpen} onOpenChange={handleOpenChange}>
        <DialogTrigger asChild>
          <Button variant="outline" size="sm" className="gap-2">
            <Settings className="h-4 w-4" />
            <span className="hidden sm:inline">Settings</span>
          </Button>
        </DialogTrigger>
                 <DialogContent className="sm:max-w-[650px] w-[95vw] max-h-none">
           <DialogHeader className="space-y-3 p-6 pb-0">
             <DialogTitle className="text-xl flex items-center gap-2">
               <Key className="h-5 w-5" />
               API Configuration
             </DialogTitle>
             <DialogDescription className="text-sm leading-relaxed text-muted-foreground">
               Configure your API keys to unlock news search and AI translation features.
               Your keys are stored securely in your browser.
             </DialogDescription>
           </DialogHeader>

           <div className="space-y-6 px-6 py-4">
            {/* Serper API Key Section */}
            <div className="space-y-3">
              <div className="flex items-center justify-between">
                <div className="space-y-0.5">
                  <label className="text-sm font-semibold flex items-center gap-2">
                    <Globe className="h-4 w-4" />
                    Serper API Key
                  </label>
                  <p className="text-xs text-muted-foreground">
                    Required for news search functionality
                  </p>
                </div>
                <a
                  href="https://serper.dev"
                  target="_blank"
                  rel="noopener noreferrer"
                  className="text-xs text-primary hover:underline flex items-center gap-1 px-3 py-1 rounded-md bg-primary/5 hover:bg-primary/10 transition-colors"
                >
                  Get API Key <ExternalLink className="h-3 w-3" />
                </a>
              </div>
              <div className="relative">
                <input
                  type={showSerperKey ? "text" : "password"}
                  value={localKeys.serperApiKey}
                  onChange={(e) => setLocalKeys(prev => ({ ...prev, serperApiKey: e.target.value }))}
                  placeholder="Enter your Serper API key..."
                  className="w-full px-4 py-3 pr-12 border rounded-lg focus:outline-none focus:ring-2 focus:ring-primary focus:border-primary transition-colors"
                />
                <Button
                  type="button"
                  variant="ghost"
                  size="sm"
                  className="absolute right-2 top-1/2 -translate-y-1/2 h-8 w-8 p-0 hover:bg-muted"
                  onClick={() => setShowSerperKey(!showSerperKey)}
                >
                  {showSerperKey ? <EyeOff className="h-4 w-4" /> : <Eye className="h-4 w-4" />}
                </Button>
              </div>
              <div className="bg-blue-50 border border-blue-200 rounded-lg p-2">
                <p className="text-xs text-blue-800">
                  <strong>Free tier:</strong> 100 searches per month • No credit card required
                </p>
              </div>
            </div>

            {/* Sutra API Key Section */}
            <div className="space-y-3">
              <div className="flex items-center justify-between">
                <div className="space-y-0.5">
                  <label className="text-sm font-semibold flex items-center gap-2">
                    <svg className="h-4 w-4" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                      <path d="M12 2L13.09 8.26L19 9L13.09 9.74L12 16L10.91 9.74L5 9L10.91 8.26L12 2Z" fill="currentColor"/>
                      <path d="M19 15L19.91 18.26L23 19L19.91 19.74L19 23L18.09 19.74L15 19L18.09 18.26L19 15Z" fill="currentColor"/>
                      <path d="M5 6L5.91 9.26L9 10L5.91 10.74L5 14L4.09 10.74L1 10L4.09 9.26L5 6Z" fill="currentColor"/>
                    </svg>
                    Sutra AI API Key
                  </label>
                  <p className="text-xs text-muted-foreground">
                    Required for AI translation to other languages
                  </p>
                </div>
                <a
                  href="https://docs.sutra.foundation"
                  target="_blank"
                  rel="noopener noreferrer"
                  className="text-xs text-primary hover:underline flex items-center gap-1 px-3 py-1 rounded-md bg-primary/5 hover:bg-primary/10 transition-colors"
                >
                  Get API Key <ExternalLink className="h-3 w-3" />
                </a>
              </div>
              <div className="relative">
                <input
                  type={showSutraKey ? "text" : "password"}
                  value={localKeys.sutraApiKey}
                  onChange={(e) => setLocalKeys(prev => ({ ...prev, sutraApiKey: e.target.value }))}
                  placeholder="Enter your Sutra API key..."
                  className="w-full px-4 py-3 pr-12 border rounded-lg focus:outline-none focus:ring-2 focus:ring-primary focus:border-primary transition-colors"
                />
                <Button
                  type="button"
                  variant="ghost"
                  size="sm"
                  className="absolute right-2 top-1/2 -translate-y-1/2 h-8 w-8 p-0 hover:bg-muted"
                  onClick={() => setShowSutraKey(!showSutraKey)}
                >
                  {showSutraKey ? <EyeOff className="h-4 w-4" /> : <Eye className="h-4 w-4" />}
                </Button>
              </div>
              <div className="bg-amber-50 border border-amber-200 rounded-lg p-2">
                <p className="text-xs text-amber-800">
                  <strong>Optional:</strong> Only needed for translating news to non-English languages
                </p>
              </div>
            </div>

            {/* Status Section */}
            <div className="bg-muted/50 rounded-xl p-4 space-y-3">
               <h4 className="text-sm font-semibold flex items-center gap-2">
                 <div className="h-2 w-2 rounded-full bg-primary"></div>
                 Configuration Status
               </h4>
               <div className="grid grid-cols-1 sm:grid-cols-2 gap-3">
                                                  <div className="flex items-center justify-between p-3 bg-background rounded-lg border shadow-sm">
                   <span className="text-sm flex items-center gap-2">
                     <Globe className="h-3 w-3" />
                     News Search
                   </span>
                   <span className={`text-xs font-medium px-2 py-1 rounded-full ${
                     apiKeys.serperApiKey 
                       ? 'bg-green-100 text-green-700 border border-green-200' 
                       : 'bg-red-100 text-red-700 border border-red-200'
                   }`}>
                     {apiKeys.serperApiKey ? 'Ready' : 'Missing'}
                   </span>
                 </div>
                 <div className="flex items-center justify-between p-3 bg-background rounded-lg border shadow-sm">
                   <span className="text-sm flex items-center gap-2">
                     <svg className="h-3 w-3" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                       <path d="M12 2L13.09 8.26L19 9L13.09 9.74L12 16L10.91 9.74L5 9L10.91 8.26L12 2Z" fill="currentColor"/>
                     </svg>
                     AI Translation
                   </span>
                   <span className={`text-xs font-medium px-2 py-1 rounded-full ${
                     apiKeys.sutraApiKey 
                       ? 'bg-green-100 text-green-700 border border-green-200' 
                       : 'bg-yellow-100 text-yellow-700 border border-yellow-200'
                   }`}>
                     {apiKeys.sutraApiKey ? 'Ready' : 'Optional'}
                   </span>
                 </div>
              </div>
            </div>
          </div>

           <div className="flex flex-col sm:flex-row gap-2 px-4 py-3 border-t bg-muted/20">
             <Button variant="outline" onClick={handleReset} className="gap-2 flex-1 sm:flex-initial h-9">
               <RotateCcw className="h-4 w-4" />
               Reset All
             </Button>
             <Button onClick={handleSave} className="gap-2 flex-1 sm:flex-initial sm:ml-auto h-9">
               <Save className="h-4 w-4" />
               Save Settings
             </Button>
           </div>
        </DialogContent>
      </Dialog>
    </>
  );
} 