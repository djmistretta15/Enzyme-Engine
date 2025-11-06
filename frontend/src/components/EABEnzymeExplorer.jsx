import React, { useState, useMemo } from 'react';
import { BarChart, Bar, PieChart, Pie, Cell, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer } from 'recharts';
import { Search, Download, X, Database, Dna, Filter, TrendingUp } from 'lucide-react';

// Sample dataset embedded
const SAMPLE_DATA = [
  { accession: "XM_018093312", enzyme: "cellulase", ec: "3.2.1.4", organism: "Agrilus planipennis", tissue: "midgut", length: 1245, source: "nucleotide", ghFamily: "GH5", confidence: 0.92, stage: "larval" },
  { accession: "XP_018098456", enzyme: "laccase", ec: "1.10.3.2", organism: "Agrilus planipennis", tissue: "gut", length: 892, source: "protein", ghFamily: null, confidence: 0.88, stage: "adult" },
  { accession: "KAF1234567", enzyme: "endoglucanase", ec: "3.2.1.4", organism: "Agrilus anxius", tissue: "midgut", length: 1156, source: "protein", ghFamily: "GH9", confidence: 0.95, stage: "larval" },
  { accession: "SRR9876543", enzyme: "peroxidase", ec: "1.11.1.7", organism: "Agrilus planipennis", tissue: "hindgut", length: 743, source: "sra", ghFamily: null, confidence: 0.81, stage: "larval" },
  { accession: "XM_019234891", enzyme: "xylanase", ec: "3.2.1.8", organism: "Chrysobothris femorata", tissue: "digestive", length: 1034, source: "nucleotide", ghFamily: "GH10", confidence: 0.87, stage: "adult" },
  { accession: "ABC9988776", enzyme: "beta-glucosidase", ec: "3.2.1.21", organism: "Agrilus planipennis", tissue: "midgut", length: 967, source: "protein", ghFamily: "GH1", confidence: 0.93, stage: "larval" },
  { accession: "XP_020445678", enzyme: "oxidase", ec: "1.3.3.4", organism: "Melanophila acuminata", tissue: "gut", length: 812, source: "protein", ghFamily: null, confidence: 0.79, stage: "adult" },
  { accession: "DEF5544332", enzyme: "mannanase", ec: "3.2.1.78", organism: "Agrilus biguttatus", tissue: "midgut", length: 1189, source: "nucleotide", ghFamily: "GH26", confidence: 0.91, stage: "larval" },
  { accession: "XM_021556789", enzyme: "cellulase", ec: "3.2.1.4", organism: "Agrilus planipennis", tissue: "foregut", length: 1298, source: "nucleotide", ghFamily: "GH7", confidence: 0.89, stage: "larval" },
  { accession: "GHI7766554", enzyme: "laccase", ec: "1.10.3.2", organism: "Chrysobothris femorata", tissue: "gut", length: 856, source: "protein", ghFamily: null, confidence: 0.84, stage: "adult" },
  { accession: "XP_022667890", enzyme: "pectinase", ec: "3.2.1.15", organism: "Agrilus anxius", tissue: "digestive", length: 1021, source: "protein", ghFamily: "GH28", confidence: 0.86, stage: "larval" },
  { accession: "JKL3322110", enzyme: "esterase", ec: "3.1.1.73", organism: "Agrilus planipennis", tissue: "midgut", length: 678, source: "protein", ghFamily: null, confidence: 0.78, stage: "adult" },
  { accession: "SRR8877665", enzyme: "endoglucanase", ec: "3.2.1.4", organism: "Melanophila acuminata", tissue: "gut", length: 1167, source: "sra", ghFamily: "GH5", confidence: 0.90, stage: "larval" },
  { accession: "MNO9988776", enzyme: "peroxidase", ec: "1.11.1.7", organism: "Agrilus planipennis", tissue: "midgut", length: 789, source: "protein", ghFamily: null, confidence: 0.82, stage: "larval" },
  { accession: "XM_023778901", enzyme: "xylanase", ec: "3.2.1.8", organism: "Agrilus anxius", tissue: "hindgut", length: 1045, source: "nucleotide", ghFamily: "GH11", confidence: 0.88, stage: "adult" },
  { accession: "PQR6655443", enzyme: "cellulase", ec: "3.2.1.4", organism: "Chrysobothris femorata", tissue: "midgut", length: 1223, source: "protein", ghFamily: "GH12", confidence: 0.94, stage: "larval" },
  { accession: "XP_024889012", enzyme: "oxidase", ec: "1.14.13.1", organism: "Agrilus planipennis", tissue: "gut", length: 834, source: "protein", ghFamily: null, confidence: 0.80, stage: "adult" },
  { accession: "STU4433221", enzyme: "glucosidase", ec: "3.2.1.21", organism: "Melanophila acuminata", tissue: "digestive", length: 945, source: "protein", ghFamily: "GH3", confidence: 0.85, stage: "larval" },
  { accession: "XM_025990123", enzyme: "laccase", ec: "1.10.3.2", organism: "Agrilus biguttatus", tissue: "midgut", length: 901, source: "nucleotide", ghFamily: null, confidence: 0.87, stage: "adult" },
  { accession: "VWX2211009", enzyme: "mannanase", ec: "3.2.1.78", organism: "Agrilus planipennis", tissue: "foregut", length: 1176, source: "protein", ghFamily: "GH26", confidence: 0.92, stage: "larval" }
];

const COLORS = {
  primary: '#284C3B',
  secondary: '#C79A4B',
  accent: '#C2C1BA',
  background: '#F5F5F5',
  charcoal: '#1F1F1F',
  chart: ['#284C3B', '#4A7C59', '#6B9E78', '#8FBE9A', '#B3D9BC', '#C79A4B', '#D4AE6A', '#E1C289']
};

export default function EABEnzymeExplorer() {
  const [searchTerm, setSearchTerm] = useState('');
  const [selectedEnzyme, setSelectedEnzyme] = useState(null);
  const [viewMode, setViewMode] = useState('table');
  const [sortConfig, setSortConfig] = useState({ key: 'confidence', direction: 'desc' });
  const [filterTissue, setFilterTissue] = useState('all');
  const [filterOrganism, setFilterOrganism] = useState('all');

  // Filtered and sorted data
  const filteredData = useMemo(() => {
    let filtered = SAMPLE_DATA.filter(item => {
      const matchesSearch =
        item.enzyme.toLowerCase().includes(searchTerm.toLowerCase()) ||
        item.organism.toLowerCase().includes(searchTerm.toLowerCase()) ||
        item.accession.toLowerCase().includes(searchTerm.toLowerCase()) ||
        (item.ec && item.ec.includes(searchTerm));

      const matchesTissue = filterTissue === 'all' || item.tissue === filterTissue;
      const matchesOrganism = filterOrganism === 'all' || item.organism === filterOrganism;

      return matchesSearch && matchesTissue && matchesOrganism;
    });

    // Sort
    if (sortConfig.key) {
      filtered.sort((a, b) => {
        if (a[sortConfig.key] < b[sortConfig.key]) return sortConfig.direction === 'asc' ? -1 : 1;
        if (a[sortConfig.key] > b[sortConfig.key]) return sortConfig.direction === 'asc' ? 1 : -1;
        return 0;
      });
    }

    return filtered;
  }, [searchTerm, sortConfig, filterTissue, filterOrganism]);

  // Chart data
  const enzymeCountData = useMemo(() => {
    const counts = {};
    filteredData.forEach(item => {
      counts[item.enzyme] = (counts[item.enzyme] || 0) + 1;
    });
    return Object.entries(counts)
      .map(([name, value]) => ({ name, value }))
      .sort((a, b) => b.value - a.value)
      .slice(0, 8);
  }, [filteredData]);

  const organismData = useMemo(() => {
    const counts = {};
    filteredData.forEach(item => {
      counts[item.organism] = (counts[item.organism] || 0) + 1;
    });
    return Object.entries(counts)
      .map(([name, value]) => ({ name: name.split(' ')[1] || name, value }))
      .sort((a, b) => b.value - a.value);
  }, [filteredData]);

  const ghFamilyData = useMemo(() => {
    const counts = {};
    filteredData.forEach(item => {
      if (item.ghFamily) {
        counts[item.ghFamily] = (counts[item.ghFamily] || 0) + 1;
      }
    });
    return Object.entries(counts)
      .map(([name, value]) => ({ name, value }))
      .sort((a, b) => b.value - a.value);
  }, [filteredData]);

  const handleSort = (key) => {
    setSortConfig(prev => ({
      key,
      direction: prev.key === key && prev.direction === 'asc' ? 'desc' : 'asc'
    }));
  };

  const exportToCSV = () => {
    const headers = ['Accession', 'Enzyme', 'EC', 'Organism', 'Tissue', 'Length', 'Source', 'GH Family', 'Confidence'];
    const csv = [
      headers.join(','),
      ...filteredData.map(item => [
        item.accession,
        item.enzyme,
        item.ec || '',
        item.organism,
        item.tissue,
        item.length,
        item.source,
        item.ghFamily || '',
        item.confidence
      ].join(','))
    ].join('\n');

    const blob = new Blob([csv], { type: 'text/csv' });
    const url = window.URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = 'eab_enzymes.csv';
    a.click();
  };

  const uniqueTissues = [...new Set(SAMPLE_DATA.map(d => d.tissue))];
  const uniqueOrganisms = [...new Set(SAMPLE_DATA.map(d => d.organism))];

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-50 to-slate-100 p-6">
      {/* Header */}
      <div className="max-w-7xl mx-auto mb-8">
        <div className="bg-gradient-to-r from-emerald-900 to-emerald-700 rounded-2xl shadow-2xl p-8 text-white">
          <div className="flex items-center justify-between">
            <div>
              <h1 className="text-4xl font-bold mb-2 flex items-center gap-3">
                <Dna className="w-10 h-10" />
                Emerald Ash Borer Enzyme Explorer
              </h1>
              <p className="text-emerald-100 text-lg">
                Interactive discovery platform for wood-digesting enzymes in <em>Agrilus planipennis</em>
              </p>
            </div>
            <div className="text-right">
              <div className="text-5xl font-bold">{filteredData.length}</div>
              <div className="text-emerald-200">Sequences</div>
            </div>
          </div>
        </div>
      </div>

      {/* Main Content */}
      <div className="max-w-7xl mx-auto">
        {/* Controls */}
        <div className="bg-white rounded-xl shadow-lg p-6 mb-6">
          <div className="grid grid-cols-1 md:grid-cols-4 gap-4 mb-4">
            <div className="md:col-span-2 relative">
              <Search className="absolute left-3 top-3 w-5 h-5 text-gray-400" />
              <input
                type="text"
                placeholder="Search enzymes, organisms, accessions..."
                value={searchTerm}
                onChange={(e) => setSearchTerm(e.target.value)}
                className="w-full pl-10 pr-4 py-2 border-2 border-gray-200 rounded-lg focus:border-emerald-500 focus:outline-none"
              />
            </div>

            <select
              value={filterTissue}
              onChange={(e) => setFilterTissue(e.target.value)}
              className="px-4 py-2 border-2 border-gray-200 rounded-lg focus:border-emerald-500 focus:outline-none"
            >
              <option value="all">All Tissues</option>
              {uniqueTissues.map(t => <option key={t} value={t}>{t}</option>)}
            </select>

            <select
              value={filterOrganism}
              onChange={(e) => setFilterOrganism(e.target.value)}
              className="px-4 py-2 border-2 border-gray-200 rounded-lg focus:border-emerald-500 focus:outline-none"
            >
              <option value="all">All Organisms</option>
              {uniqueOrganisms.map(o => <option key={o} value={o}>{o.split(' ')[1] || o}</option>)}
            </select>
          </div>

          <div className="flex gap-4">
            <button
              onClick={() => setViewMode('table')}
              className={`px-6 py-2 rounded-lg font-medium transition ${
                viewMode === 'table'
                  ? 'bg-emerald-700 text-white'
                  : 'bg-gray-100 text-gray-700 hover:bg-gray-200'
              }`}
            >
              <Database className="inline w-4 h-4 mr-2" />
              Table View
            </button>
            <button
              onClick={() => setViewMode('charts')}
              className={`px-6 py-2 rounded-lg font-medium transition ${
                viewMode === 'charts'
                  ? 'bg-emerald-700 text-white'
                  : 'bg-gray-100 text-gray-700 hover:bg-gray-200'
              }`}
            >
              <TrendingUp className="inline w-4 h-4 mr-2" />
              Visualizations
            </button>
            <button
              onClick={exportToCSV}
              className="ml-auto px-6 py-2 bg-amber-600 hover:bg-amber-700 text-white rounded-lg font-medium transition"
            >
              <Download className="inline w-4 h-4 mr-2" />
              Export CSV
            </button>
          </div>
        </div>

        {/* Table View */}
        {viewMode === 'table' && (
          <div className="bg-white rounded-xl shadow-lg overflow-hidden">
            <div className="overflow-x-auto">
              <table className="w-full">
                <thead className="bg-emerald-50 border-b-2 border-emerald-200">
                  <tr>
                    {['accession', 'enzyme', 'ec', 'organism', 'tissue', 'length', 'ghFamily', 'confidence'].map(key => (
                      <th
                        key={key}
                        onClick={() => handleSort(key)}
                        className="px-4 py-3 text-left text-sm font-semibold text-emerald-900 cursor-pointer hover:bg-emerald-100"
                      >
                        {key.charAt(0).toUpperCase() + key.slice(1).replace('ghFamily', 'GH Family')}
                        {sortConfig.key === key && (
                          <span className="ml-1">{sortConfig.direction === 'asc' ? '↑' : '↓'}</span>
                        )}
                      </th>
                    ))}
                  </tr>
                </thead>
                <tbody>
                  {filteredData.map((item, idx) => (
                    <tr
                      key={item.accession}
                      onClick={() => setSelectedEnzyme(item)}
                      className={`border-b cursor-pointer hover:bg-emerald-50 transition ${
                        idx % 2 === 0 ? 'bg-white' : 'bg-gray-50'
                      }`}
                    >
                      <td className="px-4 py-3 text-sm font-mono text-blue-600">{item.accession}</td>
                      <td className="px-4 py-3 text-sm font-medium">{item.enzyme}</td>
                      <td className="px-4 py-3 text-sm">{item.ec || '-'}</td>
                      <td className="px-4 py-3 text-sm italic">{item.organism.split(' ').slice(0, 2).join(' ')}</td>
                      <td className="px-4 py-3 text-sm">
                        <span className="px-2 py-1 bg-amber-100 text-amber-800 rounded-full text-xs">
                          {item.tissue}
                        </span>
                      </td>
                      <td className="px-4 py-3 text-sm">{item.length} bp</td>
                      <td className="px-4 py-3 text-sm font-mono">{item.ghFamily || '-'}</td>
                      <td className="px-4 py-3 text-sm">
                        <div className="flex items-center gap-2">
                          <div className="w-16 h-2 bg-gray-200 rounded-full overflow-hidden">
                            <div
                              className="h-full bg-emerald-600"
                              style={{ width: `${item.confidence * 100}%` }}
                            />
                          </div>
                          <span className="text-xs font-medium">{(item.confidence * 100).toFixed(0)}%</span>
                        </div>
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          </div>
        )}

        {/* Charts View */}
        {viewMode === 'charts' && (
          <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
            {/* Enzyme Distribution */}
            <div className="bg-white rounded-xl shadow-lg p-6">
              <h3 className="text-xl font-bold text-gray-800 mb-4">Enzyme Type Distribution</h3>
              <ResponsiveContainer width="100%" height={300}>
                <BarChart data={enzymeCountData}>
                  <CartesianGrid strokeDasharray="3 3" />
                  <XAxis dataKey="name" angle={-45} textAnchor="end" height={80} />
                  <YAxis />
                  <Tooltip />
                  <Bar dataKey="value" fill={COLORS.primary} />
                </BarChart>
              </ResponsiveContainer>
            </div>

            {/* Organism Distribution */}
            <div className="bg-white rounded-xl shadow-lg p-6">
              <h3 className="text-xl font-bold text-gray-800 mb-4">Organism Distribution</h3>
              <ResponsiveContainer width="100%" height={300}>
                <PieChart>
                  <Pie
                    data={organismData}
                    dataKey="value"
                    nameKey="name"
                    cx="50%"
                    cy="50%"
                    outerRadius={100}
                    label
                  >
                    {organismData.map((entry, index) => (
                      <Cell key={`cell-${index}`} fill={COLORS.chart[index % COLORS.chart.length]} />
                    ))}
                  </Pie>
                  <Tooltip />
                  <Legend />
                </PieChart>
              </ResponsiveContainer>
            </div>

            {/* GH Family Distribution */}
            {ghFamilyData.length > 0 && (
              <div className="bg-white rounded-xl shadow-lg p-6 lg:col-span-2">
                <h3 className="text-xl font-bold text-gray-800 mb-4">Glycoside Hydrolase (GH) Families</h3>
                <ResponsiveContainer width="100%" height={300}>
                  <BarChart data={ghFamilyData} layout="horizontal">
                    <CartesianGrid strokeDasharray="3 3" />
                    <XAxis type="number" />
                    <YAxis dataKey="name" type="category" width={60} />
                    <Tooltip />
                    <Bar dataKey="value" fill={COLORS.secondary} />
                  </BarChart>
                </ResponsiveContainer>
              </div>
            )}
          </div>
        )}

        {/* Detail Modal */}
        {selectedEnzyme && (
          <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center p-4 z-50">
            <div className="bg-white rounded-2xl shadow-2xl max-w-2xl w-full max-h-[90vh] overflow-y-auto">
              <div className="bg-gradient-to-r from-emerald-700 to-emerald-600 p-6 text-white flex justify-between items-start">
                <div>
                  <h2 className="text-2xl font-bold mb-2">{selectedEnzyme.enzyme}</h2>
                  <p className="text-emerald-100">{selectedEnzyme.accession}</p>
                </div>
                <button
                  onClick={() => setSelectedEnzyme(null)}
                  className="text-white hover:bg-white hover:bg-opacity-20 rounded-full p-2"
                >
                  <X className="w-6 h-6" />
                </button>
              </div>

              <div className="p-6 space-y-4">
                <div className="grid grid-cols-2 gap-4">
                  <div>
                    <div className="text-sm text-gray-500">Organism</div>
                    <div className="font-medium italic">{selectedEnzyme.organism}</div>
                  </div>
                  <div>
                    <div className="text-sm text-gray-500">EC Number</div>
                    <div className="font-mono">{selectedEnzyme.ec || 'Not assigned'}</div>
                  </div>
                  <div>
                    <div className="text-sm text-gray-500">Tissue Source</div>
                    <div className="font-medium">{selectedEnzyme.tissue}</div>
                  </div>
                  <div>
                    <div className="text-sm text-gray-500">Development Stage</div>
                    <div className="font-medium">{selectedEnzyme.stage}</div>
                  </div>
                  <div>
                    <div className="text-sm text-gray-500">Sequence Length</div>
                    <div className="font-medium">{selectedEnzyme.length} bp</div>
                  </div>
                  <div>
                    <div className="text-sm text-gray-500">Source Database</div>
                    <div className="font-medium uppercase">{selectedEnzyme.source}</div>
                  </div>
                  <div>
                    <div className="text-sm text-gray-500">GH Family</div>
                    <div className="font-mono font-bold">{selectedEnzyme.ghFamily || 'None'}</div>
                  </div>
                  <div>
                    <div className="text-sm text-gray-500">Confidence Score</div>
                    <div className="font-bold text-emerald-600">{(selectedEnzyme.confidence * 100).toFixed(1)}%</div>
                  </div>
                </div>

                <div className="pt-4 border-t">
                  <div className="text-sm text-gray-500 mb-2">Quick Links</div>
                  <div className="flex gap-2">
                    <button className="px-4 py-2 bg-blue-600 text-white rounded-lg text-sm hover:bg-blue-700">
                      View on NCBI
                    </button>
                    <button className="px-4 py-2 bg-emerald-600 text-white rounded-lg text-sm hover:bg-emerald-700">
                      Related Papers
                    </button>
                  </div>
                </div>
              </div>
            </div>
          </div>
        )}
      </div>
    </div>
  );
}
