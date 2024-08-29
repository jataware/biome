export type BiomeJobStatus = 'queued' | 'deferred' | 'scheduled' | 'finished' | 'started' | 'failed' | 'cancelled'
export type BiomeJob = {
    status: BiomeJobStatus,
    response?: string | object,
    queue_order: number,
    task?: string,
    url?: string,
    raw?: any
};
export type BiomeJobCollection = {[key: string]: BiomeJob}