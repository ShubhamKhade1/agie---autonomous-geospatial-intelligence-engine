import React, { useState, useEffect, useRef } from 'react';
import { 
  Activity, 
  BarChart3, 
  MessageSquare, 
  Filter, 
  RefreshCw,
  Search,
  ShieldAlert
} from 'lucide-react';
import { 
  XAxis, 
  YAxis, 
  CartesianGrid, 
  Tooltip, 
  ResponsiveContainer, 
  AreaChart, 
  Area
} from 'recharts';
import L from 'leaflet';
import 'leaflet/dist/leaflet.css';

// Mock Data
const signalData = [
  { time: '00:00', magnitude: 45, baseline: 40 },
  { time: '04:00', magnitude: 30, baseline: 35 },
  { time: '08:00', magnitude: 75, baseline: 42 },
  { time: '12:00', magnitude: 82, baseline: 45 },
  { time: '16:00', magnitude: 55, baseline: 43 },
  { time: '20:00', magnitude: 92, baseline: 41 },
];

const Dashboard = () => {
  const [query, setQuery] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [report, setReport] = useState({
    findings: "Significant deviation in sea-surface temperature (SST) relative to 3-year seasonal baseline. Magnitude exceeds historical variance by 2.4\u03C3.",
    evidence: "Anomaly validated by convergent SAR slick detection (Sentinel-1) and absence of AIS signals in the ROI, indicating potential illicit discharge.",
    recommendation: "Deploy offshore inspection vessel to ROI A-12 immediately for manual verification."
  });
  const [priorityData, setPriorityData] = useState({
    score: 88.2,
    roi: "Mumbai Coast"
  });
  
  const mapRef = useRef<HTMLDivElement>(null);
  const leafletInstance = useRef<L.Map | null>(null);

  useEffect(() => {
    // Small delay to ensure container height is settled
    const timer = setTimeout(() => {
        if (mapRef.current && !leafletInstance.current) {
            leafletInstance.current = L.map(mapRef.current, {
                center: [18.975, 72.825],
                zoom: 11,
                zoomControl: false,
                attributionControl: false
            });

            L.tileLayer('https://{s}.basemaps.cartocdn.com/dark_all/{z}/{x}/{y}{r}.png', {
                attribution: '&copy; CartoDB'
            }).addTo(leafletInstance.current);

            L.circle([18.975, 72.825], {
                color: '#0ea5e9',
                fillColor: '#0ea5e9',
                fillOpacity: 0.1,
                radius: 5000,
                weight: 1
            }).addTo(leafletInstance.current);
        }
    }, 100);

    return () => {
        clearTimeout(timer);
        if (leafletInstance.current) {
            leafletInstance.current.remove();
            leafletInstance.current = null;
        }
    };
  }, []);

  const handleQuerySubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!query.trim()) return;

    setIsLoading(true);
    try {
      const response = await fetch('http://localhost:8000/dialogue', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ query, roi_id: 'mumbai_coast' })
      });
      const data = await response.json();
      
      // Update the synthesis report with AI findings
      setReport({
        findings: data.response,
        evidence: "Verified by multi-signal convergence (Sentinel-2 + AIS).",
        recommendation: data.operator_action
      });
      
      setQuery('');
    } catch (error) {
      console.error("Dialogue Error:", error);
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="flex flex-col h-screen w-screen bg-[#020617] text-slate-100 font-sans overflow-hidden">
      {/* Header */}
      <header className="flex items-center justify-between px-6 py-4 border-b border-slate-800 bg-slate-900/50 backdrop-blur-md z-50 flex-shrink-0">
        <div className="flex items-center gap-3">
          <div className="bg-sky-600 p-2 rounded-lg shadow-lg shadow-sky-500/20">
            <Activity className="w-6 h-6" />
          </div>
          <div>
            <h1 className="text-xl font-bold tracking-tight">AGIE</h1>
            <p className="text-[10px] text-slate-400 font-medium tracking-wide leading-none mt-1 uppercase">Autonomous Geospatial Intelligence Engine</p>
          </div>
        </div>

        <div className="flex items-center gap-4">
          <div className="flex items-center gap-2 px-3 py-1 bg-slate-800/50 rounded-full border border-slate-700">
            <div className="w-2 h-2 bg-green-500 rounded-full animate-pulse"></div>
            <span className="text-[10px] uppercase font-bold tracking-tighter">NASA / Copernicus Active</span>
          </div>
          <button 
            onClick={async () => {
              setIsLoading(true);
              await fetch('http://localhost:8000/simulation/inject', { method: 'POST' });
              const res = await fetch('http://localhost:8000/anomalies/status');
              const data = await res.json();
              setPriorityData({ score: data.priority, roi: data.roi });
              setReport(prev => ({ ...prev, findings: data.status }));
              setIsLoading(false);
            }}
            className="px-3 py-1.5 bg-sky-600/20 text-sky-400 border border-sky-500/30 rounded-lg text-[10px] font-black uppercase tracking-widest hover:bg-sky-500 hover:text-white transition-all shadow-lg shadow-sky-500/10"
          >
            Trigger Simulation
          </button>
          <button className="p-2 text-slate-400 hover:text-white transition-colors">
            <RefreshCw className="w-5 h-5 transition-transform hover:rotate-180" />
          </button>
        </div>
      </header>

      {/* Main Grid */}
      <main className="flex-1 grid grid-cols-12 gap-4 p-4 min-h-0">
        
        {/* Left Column: Map & Analytics */}
        <div className="col-span-8 flex flex-col gap-4 min-h-0 overflow-hidden">
          {/* Map Layer */}
          <div className="h-[60%] bg-slate-900 rounded-2xl border border-slate-800 relative overflow-hidden shadow-2xl flex-shrink-0">
            <div ref={mapRef} className="absolute inset-0 grayscale contrast-125 opacity-90" />
            
            <div className="absolute top-4 left-4 z-[1000] flex flex-col gap-2 pointer-events-none">
              <div className="bg-slate-900/90 p-4 rounded-xl border border-slate-700 backdrop-blur-xl shadow-2xl border-l-4 border-l-sky-500">
                <div className="flex items-center gap-2 mb-2">
                  <ShieldAlert className="w-5 h-5 text-sky-400" />
                  <span className="text-sm font-black uppercase tracking-widest">{priorityData.roi}</span>
                </div>
                <div className="flex items-end gap-2">
                  <div className="text-5xl font-black text-sky-400 tabular-nums leading-none">{priorityData.score}</div>
                  <div className="text-[10px] text-slate-500 uppercase tracking-tighter mb-1 select-none font-bold">Priority Score</div>
                </div>
              </div>
            </div>
          </div>

          {/* Temporal Metrics Layer */}
          <div className="h-[40%] grid grid-cols-2 gap-4 min-h-0 pb-4">
            <div className="bg-slate-900 rounded-2xl border border-slate-800 p-6 shadow-xl flex flex-col overflow-hidden">
              <div className="flex items-center justify-between mb-2 flex-shrink-0">
                <div className="flex items-center gap-2">
                  <BarChart3 className="w-4 h-4 text-sky-400" />
                  <span className="text-xs font-black uppercase tracking-widest text-slate-400">STL Baseline Deviation</span>
                </div>
              </div>
              <div className="flex-1 min-h-[100px] w-full mt-2">
                <ResponsiveContainer width="100%" height="100%">
                  <AreaChart data={signalData}>
                    <defs>
                      <linearGradient id="colorMag" x1="0" y1="0" x2="0" y2="1">
                        <stop offset="5%" stopColor="#0ea5e9" stopOpacity={0.2}/>
                        <stop offset="95%" stopColor="#0ea5e9" stopOpacity={0}/>
                      </linearGradient>
                    </defs>
                    <CartesianGrid strokeDasharray="3 3" stroke="#1e293b" vertical={false} />
                    <XAxis dataKey="time" hide />
                    <YAxis hide domain={[0, 100]} />
                    <Tooltip contentStyle={{ backgroundColor: '#0f172a', border: 'none', borderRadius: '12px' }} />
                    <Area type="monotone" dataKey="magnitude" stroke="#0ea5e9" fill="url(#colorMag)" strokeWidth={3} />
                  </AreaChart>
                </ResponsiveContainer>
              </div>
            </div>

            <div className="bg-slate-900 rounded-2xl border border-slate-800 p-6 shadow-xl overflow-hidden flex flex-col">
               <div className="flex items-center justify-between mb-4 flex-shrink-0">
                <div className="flex items-center gap-2">
                  <Filter className="w-4 h-4 text-orange-400" />
                  <span className="text-xs font-black uppercase tracking-widest text-slate-400">Signal Convergence</span>
                </div>
              </div>
              <div className="space-y-3 overflow-y-auto pr-2">
                {[
                  { label: 'Sentinel-2 (Optical)', val: '92% Match', color: 'text-orange-400' },
                  { label: 'AIS Vessel Identity', val: 'Confirmed', color: 'text-sky-400' },
                  { label: 'MODIS Thermal Feed', val: 'Delta: 2.4\u03C3', color: 'text-green-400' }
                ].map((item, id) => (
                  <div key={id} className="flex items-center justify-between p-3 bg-[#0f172a] rounded-xl border border-slate-800 transition-all hover:bg-[#1e293b]">
                    <div className="text-[10px] font-bold uppercase tracking-wider text-slate-400">{item.label}</div>
                    <div className={`${item.color} text-xs font-black uppercase tabular-nums tracking-tighter`}>{item.val}</div>
                  </div>
                ))}
              </div>
            </div>
          </div>
        </div>

        {/* Right Column: Dialogue Layer */}
        <div className="col-span-4 flex flex-col gap-4 min-h-0 overflow-hidden mb-4">
          <div className="flex-1 bg-slate-900 rounded-2xl border border-slate-800 flex flex-col overflow-hidden shadow-2xl">
            <div className="p-6 border-b border-slate-800 flex-shrink-0 bg-slate-900/50">
               <div className="flex items-center gap-2 mb-2">
                <MessageSquare className="w-4 h-4 text-sky-400" />
                <span className="text-xs font-black uppercase tracking-widest text-slate-500">Anomaly Synthesis Engine</span>
              </div>
              <h2 className="text-xl font-bold tracking-tight">Operator Action Report</h2>
            </div>
            
            <div className="flex-1 overflow-y-auto p-6 space-y-6 min-h-0">
              <div className="space-y-4">
                <div className={`bg-[#0f172a] p-5 rounded-2xl border-l-4 border-l-sky-500 shadow-lg transition-opacity duration-300 ${isLoading ? 'opacity-50' : 'opacity-100'}`}>
                  <h4 className="text-[10px] font-black uppercase text-sky-400 mb-2 tracking-widest">Ranked Finding</h4>
                  <p className="text-sm leading-relaxed text-slate-300 italic">
                    {report.findings}
                  </p>
                </div>
                <div className={`bg-[#0f172a] p-5 rounded-2xl border-l-4 border-l-orange-500 shadow-lg transition-opacity duration-300 ${isLoading ? 'opacity-50' : 'opacity-100'}`}>
                  <h4 className="text-[10px] font-black uppercase text-orange-400 mb-2 tracking-widest">Convergent Evidence</h4>
                  <p className="text-sm leading-relaxed text-slate-300">
                    {report.evidence}
                  </p>
                </div>
                <div className={`bg-green-500/5 p-5 rounded-2xl border border-green-500/20 shadow-lg transition-opacity duration-300 ${isLoading ? 'opacity-50' : 'opacity-100'}`}>
                  <h4 className="text-[10px] font-black uppercase text-green-400 mb-2 tracking-widest">Recommended Action</h4>
                  <p className="text-sm font-bold text-green-50 leading-relaxed italic">
                    "{report.recommendation}"
                  </p>
                </div>
              </div>
            </div>

            <div className="p-4 bg-[#020617] border-t border-slate-800 flex-shrink-0">
              <form onSubmit={handleQuerySubmit} className="relative group">
                <input 
                  type="text" 
                  value={query}
                  onChange={(e) => setQuery(e.target.value)}
                  placeholder="Ask Gemini: 'What happened in ROI A-12 last week?'" 
                  className="w-full bg-slate-900 border border-slate-700 rounded-xl py-4 pl-5 pr-14 text-sm focus:ring-2 focus:ring-sky-500/50 transition-all placeholder:text-slate-600 outline-none"
                />
                <button 
                  type="submit" 
                  disabled={isLoading}
                  className="absolute right-3 top-2.5 p-2 bg-sky-600 rounded-lg shadow-lg shadow-sky-500/20 group-hover:scale-105 transition-transform disabled:bg-slate-700"
                >
                  {isLoading ? <RefreshCw className="w-5 h-5 animate-spin" /> : <Search className="w-5 h-5" />}
                </button>
              </form>
            </div>
          </div>
        </div>
      </main>
    </div>
  );
};

export default Dashboard;
