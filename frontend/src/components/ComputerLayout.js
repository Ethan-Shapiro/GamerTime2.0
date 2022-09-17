import React from "react";
import { styled } from "@mui/material/styles";
import Box from "@mui/material/Box";
import Paper from "@mui/material/Paper";
import Grid from "@mui/material/Unstable_Grid2";
import ComputerButton from "./ComputerButton";

const ComputerLayout = () => {
  return (
    <Box sx={{ flexGrow: 1 }}>
      <Grid container rowSpacing={3} columnSpacing={1}>
        <Grid xs={12}>
          <Grid container rowSpacing={1} columns={8}>
            <Grid xs={1}>
              <ComputerButton></ComputerButton>
            </Grid>
            <Grid xsOffset={2} xs={1}>
              <ComputerButton></ComputerButton>
            </Grid>
            <Grid xs={1}>
              <ComputerButton></ComputerButton>
            </Grid>
            <Grid xs={1}>
              <ComputerButton></ComputerButton>
            </Grid>
            <Grid xs={1}>
              <ComputerButton></ComputerButton>
            </Grid>
            <Grid xs={1}>
              <ComputerButton></ComputerButton>
            </Grid>
            <Grid xs={1}>
              <ComputerButton></ComputerButton>
            </Grid>
            <Grid xsOffset={2} xs={1}>
              <ComputerButton></ComputerButton>
            </Grid>
            <Grid xs={1}>
              <ComputerButton></ComputerButton>
            </Grid>
            <Grid xs={1}>
              <ComputerButton></ComputerButton>
            </Grid>
            <Grid xs={1}>
              <ComputerButton></ComputerButton>
            </Grid>
            <Grid xs={1}>
              <ComputerButton></ComputerButton>
            </Grid>
          </Grid>
        </Grid>
        <Grid xs={12}>
          <Grid container rowSpacing={1} columns={8}>
            <Grid xs={1}>
              <ComputerButton></ComputerButton>
            </Grid>
            <Grid xsOffset={2} xs={1}>
              <ComputerButton></ComputerButton>
            </Grid>
            <Grid xs={1}>
              <ComputerButton></ComputerButton>
            </Grid>
            <Grid xs={1}>
              <ComputerButton></ComputerButton>
            </Grid>
            <Grid xs={1}>
              <ComputerButton></ComputerButton>
            </Grid>
            <Grid xs={1}>
              <ComputerButton></ComputerButton>
            </Grid>
            <Grid xs={1}>
              <ComputerButton></ComputerButton>
            </Grid>
            <Grid xsOffset={2} xs={1}>
              <ComputerButton></ComputerButton>
            </Grid>
            <Grid xs={1}>
              <ComputerButton></ComputerButton>
            </Grid>
            <Grid xs={1}>
              <ComputerButton></ComputerButton>
            </Grid>
            <Grid xs={1}>
              <ComputerButton></ComputerButton>
            </Grid>
            <Grid xs={1}>
              <ComputerButton></ComputerButton>
            </Grid>
          </Grid>
        </Grid>
      </Grid>
    </Box>
  );
};

export default ComputerLayout;
