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

export interface Document {
  id: string;
  family_id: string;
  filename: string;
  uploaded_at: string;
  transactions_inserted?: number | null;
  months_upserted?: number | null;
  pipeline_result?: any;
}

/**
 * Transaction interface for the Transactions page.
 */
export interface Transaction {
  id: string;
  family_id: string;
  date: string;
  description: string;
  amount: number;
}

export interface TokenResponse {
  access_token: string;
  token_type: string;
}

export interface Scope {
  id: string;
  type: "family";
  name?: string | null;
}
