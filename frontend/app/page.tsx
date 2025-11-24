"use client";

import { useState } from "react";
import { motion, AnimatePresence } from "framer-motion";
import { Upload, FileText, CheckCircle, AlertCircle, Loader2, Sparkles, ChevronRight } from "lucide-react";
import { uploadFile, runAudit } from "@/lib/api";
import clsx from "clsx";

export default function Home() {
  const [file, setFile] = useState<File | null>(null);
  const [status, setStatus] = useState<"idle" | "uploading" | "processing" | "success" | "error">("idle");
  const [result, setResult] = useState<any>(null);
  const [errorMsg, setErrorMsg] = useState("");

  const handleFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    if (e.target.files && e.target.files[0]) {
      setFile(e.target.files[0]);
      setStatus("idle");
      setResult(null);
    }
  };

  const handleProcess = async () => {
    if (!file) return;

    try {
      setStatus("uploading");
      await uploadFile(file);

      setStatus("processing");
      const data = await runAudit();
      
      setResult(data);
      setStatus("success");
    } catch (err) {
      console.error(err);
      setStatus("error");
      setErrorMsg("Failed to process document. Please try again.");
    }
  };

  return (
    <main className="min-h-screen bg-[#F5F5F7] text-[#1D1D1F] font-sans selection:bg-blue-500/20">
      <div className="max-w-5xl mx-auto px-6 py-20">
        
        {/* Header */}
        <motion.div 
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          className="text-center mb-16"
        >
          <div className="inline-flex items-center justify-center p-3 mb-6 bg-white rounded-2xl shadow-sm border border-gray-100">
            <Sparkles className="w-6 h-6 text-blue-600 mr-2" />
            <span className="font-medium text-gray-600">AI Powered Audit</span>
          </div>
          <h1 className="text-5xl md:text-7xl font-semibold tracking-tight mb-6 bg-clip-text text-transparent bg-gradient-to-b from-gray-900 to-gray-600">
            R&D Project Auditor
          </h1>
          <p className="text-xl text-gray-500 max-w-2xl mx-auto leading-relaxed">
            Upload your PUR documents and let our advanced RAG engine analyze compliance, innovation, and financial viability in seconds.
          </p>
        </motion.div>

        {/* Main Card */}
        <motion.div 
          initial={{ opacity: 0, scale: 0.95 }}
          animate={{ opacity: 1, scale: 1 }}
          transition={{ delay: 0.1 }}
          className="bg-white rounded-[32px] shadow-2xl shadow-gray-200/50 border border-white/50 overflow-hidden backdrop-blur-xl"
        >
          <div className="p-8 md:p-12">
            
            {/* Upload Section */}
            <div className="flex flex-col items-center justify-center border-2 border-dashed border-gray-200 rounded-2xl p-12 transition-colors hover:border-blue-400 hover:bg-blue-50/30 group cursor-pointer relative">
              <input 
                type="file" 
                accept=".pdf"
                onChange={handleFileChange}
                className="absolute inset-0 w-full h-full opacity-0 cursor-pointer z-10"
              />
              <div className="w-16 h-16 bg-blue-50 rounded-full flex items-center justify-center mb-4 group-hover:scale-110 transition-transform">
                <Upload className="w-8 h-8 text-blue-600" />
              </div>
              <h3 className="text-xl font-medium mb-2">
                {file ? file.name : "Drop your PDF here"}
              </h3>
              <p className="text-gray-400">
                {file ? "Click to change file" : "or click to browse"}
              </p>
            </div>

            {/* Action Button */}
            <div className="mt-8 flex justify-center">
              <button
                onClick={handleProcess}
                disabled={!file || status === "uploading" || status === "processing"}
                className={clsx(
                  "px-8 py-4 rounded-full font-medium text-lg transition-all flex items-center shadow-lg hover:shadow-xl active:scale-95",
                  !file ? "bg-gray-100 text-gray-400 cursor-not-allowed" : "bg-black text-white hover:bg-gray-800"
                )}
              >
                {status === "uploading" && <><Loader2 className="w-5 h-5 mr-2 animate-spin" /> Uploading...</>}
                {status === "processing" && <><Loader2 className="w-5 h-5 mr-2 animate-spin" /> Analyzing...</>}
                {status === "idle" || status === "success" || status === "error" ? (
                  <>Start Analysis<ChevronRight className="w-5 h-5 ml-2" /></>
                ) : null}
              </button>
            </div>

            {/* Error Message */}
            {status === "error" && (
              <motion.div 
                initial={{ opacity: 0, y: 10 }}
                animate={{ opacity: 1, y: 0 }}
                className="mt-6 p-4 bg-red-50 text-red-600 rounded-xl flex items-center justify-center"
              >
                <AlertCircle className="w-5 h-5 mr-2" />
                {errorMsg}
              </motion.div>
            )}
          </div>

          {/* Results Section */}
          <AnimatePresence>
            {result && (
              <motion.div 
                initial={{ height: 0, opacity: 0 }}
                animate={{ height: "auto", opacity: 1 }}
                exit={{ height: 0, opacity: 0 }}
                className="border-t border-gray-100 bg-gray-50/50"
              >
                <div className="p-8 md:p-12">
                  <div className="flex items-center justify-between mb-8">
                    <h2 className="text-2xl font-semibold">Audit Report</h2>
                    <div className={clsx(
                      "px-4 py-1 rounded-full text-sm font-medium border",
                      result.risk_assessment === "Baixo" ? "bg-green-100 text-green-700 border-green-200" :
                      result.risk_assessment === "Médio" ? "bg-yellow-100 text-yellow-700 border-yellow-200" :
                      "bg-red-100 text-red-700 border-red-200"
                    )}>
                      Risk: {result.risk_assessment}
                    </div>
                  </div>

                  <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
                    {/* Score Card */}
                    <div className="col-span-1 md:col-span-1 bg-white p-6 rounded-2xl border border-gray-100 shadow-sm flex flex-col items-center justify-center">
                      <h3 className="text-sm font-medium text-gray-400 uppercase tracking-wider mb-4">Compliance Score</h3>
                      <div className="relative w-32 h-32 flex items-center justify-center">
                        <svg className="w-full h-full transform -rotate-90">
                          <circle cx="64" cy="64" r="56" stroke="#F3F4F6" strokeWidth="12" fill="transparent" />
                          <circle cx="64" cy="64" r="56" stroke={result.compliance_score > 70 ? "#10B981" : result.compliance_score > 40 ? "#F59E0B" : "#EF4444"} strokeWidth="12" fill="transparent" strokeDasharray={351.86} strokeDashoffset={351.86 - (351.86 * result.compliance_score) / 100} className="transition-all duration-1000 ease-out" />
                        </svg>
                        <span className="absolute text-3xl font-bold text-gray-800">{result.compliance_score}</span>
                      </div>
                    </div>

                    {/* Key Metrics */}
                    <div className="col-span-1 md:col-span-2 grid grid-cols-1 sm:grid-cols-2 gap-6">
                      <ResultCard title="Project Title" value={result.project_title} icon={<FileText className="w-5 h-5 text-blue-500" />} />
                      <ResultCard title="TRL Level" value={`Level ${result.trl_level}`} icon={<CheckCircle className="w-5 h-5 text-purple-500" />} />
                      <ResultCard title="Risk Assessment" value={result.risk_assessment} icon={<AlertCircle className={clsx("w-5 h-5", result.risk_assessment === "Baixo" ? "text-green-500" : result.risk_assessment === "Médio" ? "text-yellow-500" : "text-red-500")} />} />
                      <ResultCard title="Financial Analysis" value={result.financial_analysis} icon={<Sparkles className="w-5 h-5 text-yellow-500" />} />
                    </div>

                    {/* Full Width Sections */}
                    <ResultCard title="Team Analysis" value={result.team_analysis} fullWidth />
                    <ResultCard title="Methodology" value={result.methodology_summary} fullWidth />
                    
                    <div className="col-span-1 md:col-span-3 bg-white p-6 rounded-2xl border border-gray-100 shadow-sm">
                      <h3 className="text-sm font-medium text-gray-400 uppercase tracking-wider mb-4 flex items-center">
                        <Sparkles className="w-4 h-4 mr-2 text-blue-500" /> Innovation Highlights
                      </h3>
                      <ul className="grid grid-cols-1 md:grid-cols-2 gap-4">
                        {result.innovation_highlights.map((item: string, i: number) => (
                          <li key={i} className="flex items-start p-3 bg-blue-50/50 rounded-xl">
                            <span className="w-2 h-2 bg-blue-500 rounded-full mt-2 mr-3 flex-shrink-0" />
                            <span className="text-gray-700 text-sm leading-relaxed">{item}</span>
                          </li>
                        ))}
                      </ul>
                    </div>

                    <ResultCard title="Justification" value={result.justification} fullWidth />
                  </div>
                </div>
              </motion.div>
            )}
          </AnimatePresence>
        </motion.div>
      </div>
    </main>
  );
}

function ResultCard({ title, value, icon, fullWidth = false }: { title: string, value: string, icon?: React.ReactNode, fullWidth?: boolean }) {
  return (
    <div className={clsx("bg-white p-6 rounded-2xl border border-gray-100 shadow-sm", fullWidth ? "col-span-1 md:col-span-2" : "")}>
      <div className="flex items-center mb-3">
        {icon}
        <h3 className={clsx("text-sm font-medium text-gray-400 uppercase tracking-wider", icon && "ml-2")}>{title}</h3>
      </div>
      <p className="text-gray-800 font-medium leading-relaxed">{value}</p>
    </div>
  );
}
