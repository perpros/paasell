// src/components/common/Form/index.tsx
import { Box } from '@mui/material';

interface FormProps {
  onSubmit: (e: React.FormEvent<HTMLFormElement>) => void;
  children: React.ReactNode;
}

export const Form = ({ onSubmit, children }: FormProps) => {
  return (
    <Box component="form" onSubmit={onSubmit} noValidate autoComplete="off">
      {children}
    </Box>
  );
};
