// @trace TASK-018
// @trace TASK-041
import { useState } from 'react';

interface CampaignFormProps {
  onSuccess?: (campaignId: number) => void;
}

export function CampaignForm({ onSuccess }: CampaignFormProps) {
  const [name, setName] = useState('');
  const [description, setDescription] = useState('');
  const [partySize, setPartySize] = useState(4);
  const [partyLevel, setPartyLevel] = useState(1);
  const [error, setError] = useState<string | null>(null);
  const [loading, setLoading] = useState(false);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError(null);
    setLoading(true);

    const token = localStorage.getItem('token');
    if (!token) {
      setError('You must be logged in to create a campaign.');
      setLoading(false);
      return;
    }

    try {
      const response = await fetch('/campaigns', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${token}`
        },
        body: JSON.stringify({
          name,
          description,
          party_size: partySize,
          party_level: partyLevel
        })
      });

      if (!response.ok) {
        const data = await response.json();
        throw new Error(data.detail || 'Failed to create campaign');
      }

      const data = await response.json();
      if (onSuccess) {
        onSuccess(data.id);
      }
      
      // Reset form
      setName('');
      setDescription('');
      setPartySize(4);
      setPartyLevel(1);
      
    // eslint-disable-next-line @typescript-eslint/no-explicit-any
    } catch (err: any) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="max-w-md mx-auto bg-fantasy-dark border border-fantasy-accent p-6 rounded shadow-lg shadow-fantasy-accent/20">
      <h2 className="text-2xl font-bold mb-6 text-fantasy-accent uppercase tracking-wider text-center">New Campaign</h2>
      
      {error && (
        <div className="mb-4 p-3 bg-red-900/50 border border-red-500 text-red-200 rounded text-sm">
          {error}
        </div>
      )}

      <form onSubmit={handleSubmit} className="space-y-4">
        <div>
          <label className="block text-fantasy-text text-sm font-bold mb-2 uppercase tracking-wide">
            Campaign Name
          </label>
          <input
            type="text"
            value={name}
            onChange={(e) => setName(e.target.value)}
            className="w-full bg-black/50 border border-fantasy-accent/50 rounded px-3 py-2 text-fantasy-text focus:outline-none focus:border-fantasy-accent transition-colors"
            required
            placeholder="E.g., Abomination Vaults"
          />
        </div>

        <div>
          <label className="block text-fantasy-text text-sm font-bold mb-2 uppercase tracking-wide">
            Description
          </label>
          <textarea
            value={description}
            onChange={(e) => setDescription(e.target.value)}
            className="w-full bg-black/50 border border-fantasy-accent/50 rounded px-3 py-2 text-fantasy-text focus:outline-none focus:border-fantasy-accent transition-colors h-24 resize-none"
            placeholder="A brief summary of your adventure..."
          />
        </div>

        <div className="flex gap-4">
          <div className="flex-1">
            <label className="block text-fantasy-text text-sm font-bold mb-2 uppercase tracking-wide">
              Party Size
            </label>
            <input
              type="number"
              min="1"
              max="12"
              value={partySize}
              onChange={(e) => setPartySize(parseInt(e.target.value) || 4)}
              className="w-full bg-black/50 border border-fantasy-accent/50 rounded px-3 py-2 text-fantasy-text focus:outline-none focus:border-fantasy-accent transition-colors"
              required
            />
          </div>
          
          <div className="flex-1">
            <label className="block text-fantasy-text text-sm font-bold mb-2 uppercase tracking-wide">
              Party Level
            </label>
            <input
              type="number"
              min="1"
              max="20"
              value={partyLevel}
              onChange={(e) => setPartyLevel(parseInt(e.target.value) || 1)}
              className="w-full bg-black/50 border border-fantasy-accent/50 rounded px-3 py-2 text-fantasy-text focus:outline-none focus:border-fantasy-accent transition-colors"
              required
            />
          </div>
        </div>

        <button
          type="submit"
          disabled={loading}
          className="w-full bg-fantasy-accent text-fantasy-dark font-bold uppercase tracking-widest py-3 rounded mt-6 hover:bg-fantasy-text transition-colors disabled:opacity-50"
        >
          {loading ? 'Forging Campaign...' : 'Forge Campaign'}
        </button>
      </form>
    </div>
  );
}
