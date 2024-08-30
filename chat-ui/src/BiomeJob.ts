export type BiomeJobStatus = 
    | 'queued' 
    | 'deferred' 
    | 'scheduled' 
    | 'finished' 
    | 'started' 
    | 'failed' 
    | 'cancelled'
    | 'awaiting_user_input' // precondition: started 

export type BiomeJob = {
    status: BiomeJobStatus,
    response?: string | object,
    queue_order: number,
    task?: string,
    url?: string,
    raw?: any
    logs?: string[];
};
export type BiomeJobCollection = {[key: string]: BiomeJob}

export const biomeJobColorMap: {[key in BiomeJobStatus]: string} = {
    started: 'primary',
    cancelled: 'warning',
    deferred: 'warning',
    failed: 'danger',
    finished: 'success',
    queued: 'secondary',
    scheduled: 'secondary',
    awaiting_user_input: 'info'
}

// greedy take first as overall indicator 
// - one error should be prioritized over all successes at a glance
// - user input is most important
export const biomeJobColorSeverity: BiomeJobStatus[] = [
    "awaiting_user_input",
    "failed",
    "started",
    "finished",
    "queued"
];

// for a group of jobs, summarize to the most important color above
export const getJobGroupColor = (jobs: BiomeJobCollection): string => {
    const jobStatuses = Object.entries(jobs).map(([_, {status}]) => status);
    for (const status of biomeJobColorSeverity) {
        if (jobStatuses.includes(status)) {
            console.log(status);
            return biomeJobColorMap[status];
        }
    }
    return 'primary';
}