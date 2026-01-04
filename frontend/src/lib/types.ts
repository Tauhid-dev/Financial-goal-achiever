/**
 * TypeScript interfaces mirroring backend response shapes.
 */

export interface GoalCreate {
  name: string;
  target_amount: number;
  current_amount?: number;
  monthly_contribution?: number;
  target_date?: string | null;
}

export interface GoalProjection {
  months_required: number;
  years_required: number;
  is_achievable: boolean;
}

export interface GoalWithProjection extends GoalCreate {
  id: string;
  family_id: string;
  projection?: GoalProjection | null;
}

export interface MonthlySummary {
  id: string;
  family_id: string;
  month: string;
  income: number;
  expenses: number;
  savings: number;
  savings_rate: number;
}

export interface TokenResponse {
  access_token: string;
  token_type: string;
}
