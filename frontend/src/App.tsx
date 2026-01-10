import React from "react";
import AuthGate from "./components/AuthGate";
import AppHome from "./pages/AppHome";

export default function App() {
  return (
    <AuthGate>
      <AppHome />
    </AuthGate>
  );
}
