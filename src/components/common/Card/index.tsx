// src/components/common/Card/index.tsx
import { Card as MUICard, CardContent, Typography } from '@mui/material';

interface CardProps {
  title: string;
  children: React.ReactNode;
}

export const Card = ({ title, children }: CardProps) => {
  return (
    <MUICard>
      <CardContent>
        <Typography variant="h5" component="div">
          {title}
        </Typography>
        {children}
      </CardContent>
    </MUICard>
  );
};
