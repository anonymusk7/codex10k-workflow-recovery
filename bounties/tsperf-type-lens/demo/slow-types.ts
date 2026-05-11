type Primitive = string | number | boolean | Date;

type Expand<T> = T extends object ? { [K in keyof T]: Expand<T[K]> } : T;

type Variant<N extends string, Payload> = {
  kind: N;
  payload: Payload;
  meta: {
    createdAt: Date;
    source: "import" | "api" | "manual";
    flags: Record<string, boolean>;
  };
};

type DeepRecord<T> = {
  [K in "alpha" | "beta" | "gamma" | "delta" | "epsilon"]: {
    current: T;
    previous?: T;
    history: Array<{ value: T; at: Date; actor: string }>;
  };
};

type LargeUnion =
  | Variant<"contact", DeepRecord<{ email: string; phone?: string; tags: string[] }>>
  | Variant<"invoice", DeepRecord<{ amount: number; currency: "USD" | "EUR" | "GBP"; paid: boolean }>>
  | Variant<"ticket", DeepRecord<{ priority: "low" | "medium" | "high"; notes: string[] }>>
  | Variant<"event", DeepRecord<{ startsAt: Date; attendees: Array<{ id: string; role: string }> }>>;

export type SlowCustomerState = Expand<
  LargeUnion & {
    audit: Array<Variant<"audit", { path: string; before: Primitive; after: Primitive }>>;
    permissions: Record<"owner" | "editor" | "viewer", { allowed: boolean; scopes: string[] }>;
  }
>;

export interface DashboardRow {
  id: string;
  state: SlowCustomerState;
  render(): Promise<SlowCustomerState>;
}

export const row = {} as DashboardRow;
