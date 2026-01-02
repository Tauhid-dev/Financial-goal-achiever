/**
 * TypeScript interfaces mirroring backend response shapes.
 */

export interface Token {
  access_token: string;
  token_type: string;
}

export interface UserRead {
  id: number;
  email: string;
  is_active: boolean;
  is_superuser: boolean;
  // add other fields as needed
}

export interface GoalCreate {
  title: string;
  target_amount: number;
  // add other fields required by backend schema
}

export interface GoalWithProjection extends GoalCreate {
  id: number;
  // projection fields (e.g., progress, remaining) can be added here
}
