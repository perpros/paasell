import * as React from 'react';

interface FormProps {
  children: React.ReactNode;
  onSubmit: (event: React.FormEvent<HTMLFormElement>) => void;
}

export default function Form({ children, onSubmit }: FormProps) {
  return <form onSubmit={onSubmit}>{children}</form>;
}
