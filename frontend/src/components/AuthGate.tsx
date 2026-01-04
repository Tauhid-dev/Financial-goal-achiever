import React, { ReactNode } from "react";
import { Login } from "../pages/Login";

interface Props {
  children: ReactNode;
}

export default function AuthGate({ children }: Props) {
  const token = localStorage.getItem("token");
  return token ? <>{children}</> : <Login />;
}
