// @trace TASK-043
import { useState, useEffect } from 'react';

interface Campaign {
  id: number;
  name: string;
  description: string | null;
  party_size: number;
  party_level: number;
  created_at: string;
  gm_user_id: number;
}

interface GlobalCampaignListProps {
  onSelectCampaign: (id: number) => void;
}

export function GlobalCampaignList({ onSelectCampaign }: GlobalCampaignListProps) {
  const [campaigns, setCampaigns] = useState<Campaign[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const fetchCampaigns = async () => {
      try {
        const response = await fetch('/campaigns/all');

        if (!response.ok) {
          throw new Error('Failed to fetch global campaigns');
        }

        const data = await response.json();
        setCampaigns(data);
      // eslint-disable-next-line @typescript-eslint/no-explicit-any
      } catch (err: any) {
        setError(err.message);
      } finally {
        setLoading(false);
      }
    };

    fetchCampaigns();
  }, []);

  if (loading) {
    return <div className="text-center text-fantasy-accent animate-pulse">Loading global campaigns...</div>;
  }

  if (error) {
    return <div className="text-red-500 text-center">{error}</div>;
  }

  return (
    <div className="max-w-4xl mx-auto">
      <div className="flex justify-between items-center mb-6 border-b border-fantasy-accent/30 pb-4">
        <h2 className="text-2xl font-bold text-fantasy-accent uppercase tracking-wider">Global Campaigns</h2>
      </div>

      {campaigns.length === 0 ? (
        <div className="text-center p-8 bg-black/40 border border-fantasy-accent/30 rounded text-fantasy-text/60">
          No campaigns have been forged yet.
        </div>
      ) : (
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          {campaigns.map(campaign => (
            <div 
              key={campaign.id} 
              className="bg-fantasy-dark border border-fantasy-accent/50 p-5 rounded hover:border-fantasy-accent transition-colors cursor-pointer"
              onClick={() => onSelectCampaign(campaign.id)}
            >
              <h3 className="text-xl font-bold text-fantasy-text mb-2">{campaign.name}</h3>
              {campaign.description && (
                <p className="text-fantasy-text/80 text-sm mb-4 line-clamp-2">{campaign.description}</p>
              )}
              <div className="flex justify-between text-xs text-fantasy-accent/70 font-bold uppercase tracking-wider">
                <span>Party: {campaign.party_size}</span>
                <span>Level: {campaign.party_level}</span>
                <span>GM ID: {campaign.gm_user_id}</span>
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  );
}