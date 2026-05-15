// @trace TASK-041
// @trace TASK-023
import { TimelineView } from './TimelineView';

interface CampaignDashboardProps {
  campaignId: number;
  onBack: () => void;
}

export function CampaignDashboard({ campaignId, onBack }: CampaignDashboardProps) {
  return (
    <div className="max-w-6xl mx-auto bg-fantasy-dark border border-fantasy-accent p-8 rounded shadow-lg shadow-fantasy-accent/20 text-fantasy-text">
      <button 
        onClick={onBack}
        className="mb-6 text-fantasy-accent hover:text-fantasy-text transition-colors text-sm uppercase tracking-wider font-bold"
      >
        &larr; Back to GM Dashboard
      </button>
      
      <h2 className="text-3xl font-bold mb-8 text-fantasy-accent uppercase tracking-wider border-b border-fantasy-accent/30 pb-4">
        Campaign #{campaignId} Dashboard
      </h2>
      
      <div className="space-y-6">
        <section className="bg-black/40 border border-fantasy-accent/30 p-6 rounded">
          <h3 className="text-xl font-bold mb-4 text-fantasy-accent">Timeline</h3>
          <TimelineView campaignId={campaignId} />
        </section>
      </div>
    </div>
  );
}