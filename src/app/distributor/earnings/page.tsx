'use client';

import { Card } from '@/components/common/Card';
import { Box, Grid, Typography } from '@mui/material';

export default function EarningsPage() {
  return (
    <Box>
      <Typography variant="h4" gutterBottom>
        Earnings Dashboard
      </Typography>
      <Grid container spacing={3}>
        <Grid item xs={12} md={4}>
          <Card title="Total Earnings">
            <Typography variant="h5">$5,000</Typography>
          </Card>
        </Grid>
        <Grid item xs={12} md={4}>
          <Card title="Total Clicks">
            <Typography variant="h5">10,000</Typography>
          </Card>
        </Grid>
        <Grid item xs={12} md={4}>
          <Card title="Conversion Rate">
            <Typography variant="h5">5%</Typography>
          </Card>
        </Grid>
      </Grid>
    </Box>
  );
}
