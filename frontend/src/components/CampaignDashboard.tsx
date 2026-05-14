// @trace TASK-041

interface CampaignDashboardProps {
  campaignId: number;
  onBack: () => void;
}

export function CampaignDashboard({ campaignId, onBack }: CampaignDashboardProps) {
  return (
    <div className="max-w-4xl mx-auto bg-fantasy-dark border border-fantasy-accent p-8 rounded shadow-lg shadow-fantasy-accent/20 text-fantasy-text">
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
          
          <div className="space-y-4">
            {/* Initial timeline tick mocked as per FCHAIN-002 requirements since backend timeline service isn't fully implemented */}
            <div className="flex gap-4 items-start">
              <div className="w-16 flex-shrink-0 text-center text-fantasy-accent/60 font-bold border-r border-fantasy-accent/30 pr-4">
                Tick 1
              </div>
              <div className="flex-1">
                <p className="text-lg">The campaign begins.</p>
                <p className="text-sm text-fantasy-text/60 mt-1">System Generated</p>
              </div>
            </div>
          </div>
        </section>
      </div>
    </div>
  );
}