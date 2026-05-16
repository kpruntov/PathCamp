// @trace TASK-023
import { useState, useEffect } from 'react';

interface Asset {
  id: number;
  tick_id: number;
  asset_type: string;
  name: string;
  description: string | null;
  traits: string[] | null;
}

interface Tick {
  id: number;
  tick_number: int;
  narrative: string | null;
  assets: Asset[];
}

interface TimelineData {
  campaign_id: int;
  is_owner: boolean;
  ticks: Tick[];
}

interface TimelineViewProps {
  campaignId: number;
}

export function TimelineView({ campaignId }: TimelineViewProps) {
  const [timeline, setTimeline] = useState<TimelineData | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [newTickNarrative, setNewTickNarrative] = useState('');
  const [submitting, setSubmitting] = useState(false);
  const [selectedTick, setSelectedTick] = useState<Tick | null>(null);
  const [editNarrative, setEditNarrative] = useState('');

  const fetchTimeline = () => {
    fetch(`/campaigns/${campaignId}/timeline`, {
      headers: {
        'Authorization': `Bearer ${localStorage.getItem('token')}`
      }
    })
    .then(res => {
      if (!res.ok) throw new Error('Failed to fetch timeline');
      return res.json();
    })
    .then(data => {
      setTimeline(data);
      setError(null);
    })
    .catch(err => setError(err.message))
    .finally(() => setLoading(false));
  };

  useEffect(() => {
    // eslint-disable-next-line react-hooks/set-state-in-effect
    setLoading(true);
    fetchTimeline();
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [campaignId]);

  const handleCreateTick = (e: React.FormEvent) => {
    e.preventDefault();
    if (!newTickNarrative.trim()) return;

    setSubmitting(true);
    fetch('/ticks', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${localStorage.getItem('token')}`
      },
      body: JSON.stringify({ campaign_id: campaignId, narrative: newTickNarrative })
    })
    .then(res => {
      if (!res.ok) throw new Error('Failed to create tick');
      setNewTickNarrative('');
      fetchTimeline();
    })
    .catch(err => alert(err.message))
    .finally(() => setSubmitting(false));
  };

  const handleUpdateTick = (e: React.FormEvent) => {
    e.preventDefault();
    if (!selectedTick) return;

    setSubmitting(true);
    fetch(`/ticks/${selectedTick.id}`, {
      method: 'PUT',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${localStorage.getItem('token')}`
      },
      body: JSON.stringify({ narrative: editNarrative })
    })
    .then(res => {
      if (!res.ok) throw new Error('Failed to update tick');
      setSelectedTick(null);
      fetchTimeline();
    })
    .catch(err => alert(err.message))
    .finally(() => setSubmitting(false));
  };

  if (loading) return <div className="text-fantasy-accent">Loading timeline...</div>;
  if (error) return <div className="text-red-500">Error: {error}</div>;

  return (
    <div className="flex gap-6 relative">
      {/* Timeline List */}
      <div className="flex-1 space-y-6 max-h-[800px] overflow-y-auto pr-4 custom-scrollbar">
        {timeline?.ticks.map((tick) => (
          <div 
            key={tick.id} 
            className={`border rounded p-4 cursor-pointer transition-colors ${selectedTick?.id === tick.id ? 'border-fantasy-accent bg-fantasy-accent/10' : 'border-fantasy-accent/30 bg-black/40 hover:border-fantasy-accent/60'}`}
            onClick={() => { setSelectedTick(tick); setEditNarrative(tick.narrative || ''); }}
          >
            <div className="flex gap-4 items-start">
              <div className="w-16 flex-shrink-0 text-center text-fantasy-accent/80 font-bold border-r border-fantasy-accent/30 pr-4">
                Tick {tick.tick_number}
              </div>
              <div className="flex-1">
                <p className="text-lg whitespace-pre-wrap">{tick.narrative || 'No narrative'}</p>
                {tick.assets && tick.assets.length > 0 && (
                  <div className="mt-4 flex flex-wrap gap-2">
                    {tick.assets.map(asset => (
                      <span key={asset.id} className="text-xs px-2 py-1 bg-fantasy-accent/20 text-fantasy-accent rounded border border-fantasy-accent/30">
                        {asset.name} ({asset.asset_type})
                      </span>
                    ))}
                  </div>
                )}
              </div>
            </div>
          </div>
        ))}

        {/* New Tick Form */}
        {timeline?.is_owner && (
          <form onSubmit={handleCreateTick} className="bg-black/60 border border-fantasy-accent p-4 rounded mt-8">
            <h4 className="text-fantasy-accent font-bold mb-4 uppercase tracking-wide text-sm">Add Next Tick</h4>
            <textarea
              value={newTickNarrative}
              onChange={(e) => setNewTickNarrative(e.target.value)}
              className="w-full bg-black/50 border border-fantasy-accent/30 rounded p-3 text-fantasy-text focus:border-fantasy-accent focus:outline-none min-h-[100px]"
              placeholder="Describe what happens next..."
              required
            />
            <button
              type="submit"
              disabled={submitting}
              className="mt-4 bg-fantasy-accent text-fantasy-dark px-4 py-2 rounded font-bold uppercase tracking-wide text-sm hover:bg-fantasy-text transition-colors disabled:opacity-50"
            >
              {submitting ? 'Adding...' : 'Create Tick'}
            </button>
          </form>
        )}
      </div>

      {/* Side Panel for Editing */}
      {selectedTick && timeline?.is_owner && (
        <div className="w-80 flex-shrink-0 bg-black/60 border border-fantasy-accent rounded p-6 sticky top-0 h-fit">
          <div className="flex justify-between items-center mb-6">
            <h3 className="text-xl font-bold text-fantasy-accent uppercase tracking-wide">Tick {selectedTick.tick_number}</h3>
            <button onClick={() => setSelectedTick(null)} className="text-fantasy-text/60 hover:text-fantasy-text">
              ✕
            </button>
          </div>
          
          <form onSubmit={handleUpdateTick}>
            <label className="block text-sm text-fantasy-accent mb-2">Narrative</label>
            <textarea
              value={editNarrative}
              onChange={(e) => setEditNarrative(e.target.value)}
              className="w-full bg-black/50 border border-fantasy-accent/30 rounded p-3 text-fantasy-text focus:border-fantasy-accent focus:outline-none min-h-[200px] mb-4"
              required
            />
            <button
              type="submit"
              disabled={submitting}
              className="w-full bg-fantasy-accent text-fantasy-dark px-4 py-2 rounded font-bold uppercase tracking-wide text-sm hover:bg-fantasy-text transition-colors disabled:opacity-50"
            >
              {submitting ? 'Saving...' : 'Update Tick'}
            </button>
          </form>

          {/* Further implementation for assets could go here */}
          <div className="mt-8 border-t border-fantasy-accent/30 pt-4">
            <h4 className="text-sm font-bold text-fantasy-accent mb-2">Assets in Tick</h4>
            {selectedTick.assets.length === 0 ? (
              <p className="text-sm text-fantasy-text/60">No assets</p>
            ) : (
              <ul className="space-y-2">
                {selectedTick.assets.map(asset => (
                  <li key={asset.id} className="text-sm bg-black/40 p-2 rounded border border-fantasy-accent/20">
                    <strong>{asset.name}</strong> <span className="text-fantasy-text/60">({asset.asset_type})</span>
                  </li>
                ))}
              </ul>
            )}
          </div>
        </div>
      )}
    </div>
  );
}
