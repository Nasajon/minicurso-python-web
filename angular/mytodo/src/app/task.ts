export interface Task {
    id: string;
    description: string;
    priority: number;
    complexity: number;
    created_at: string;
    finished_at: string;
    time: number;
    status: boolean;
}