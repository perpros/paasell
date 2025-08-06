import * as React from 'react';
import MuiCard from '@mui/material/Card';
import CardContent from '@mui/material/CardContent';
import CardHeader from '@mui/material/CardHeader';

interface CardProps {
  title?: string;
  children: React.ReactNode;
}

export default function Card({ title, children }: CardProps) {
  return (
    <MuiCard>
      {title && <CardHeader title={title} />}
      <CardContent>{children}</CardContent>
    </MuiCard>
  );
}
