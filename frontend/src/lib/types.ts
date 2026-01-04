/**
 * TypeScript interfaces mirroring backend response shapes.
 */

export interface GoalCreate {
  name: string;
  target_amount: number;
  current_amount: number;
  monthly_contribution: number;
  target_date?: string; // ISO date string, optional
}

export interface GoalProjection {
  months_required: number;
  years_required: number;
  is_achievable: boolean;
}

export interface GoalWithProjection extends GoalCreate {
  id: number;
  family_id: number;
  projection?: GoalProjection | null;
}

export interface MonthlySummary {
  id: number;
  family_id: number;
  month: string; // e.g., "2024-01"
  income: number;
  expenses: number;
  savings: number;
  savings_rate: number;
}

export interface TokenResponse {
  access_token: string;
  token_type: string;
}
