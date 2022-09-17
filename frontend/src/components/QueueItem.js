import React from "react";
import { Box, Grid, IconButton } from "@mui/material";
import DeleteIcon from "@mui/icons-material/Delete";
const QueueItem = ({ name, computerID, deleteFunc, itemID }) => {
  return (
    <Grid sx={{}} container>
      <Grid sx={{ border: 1 }} xs={8}>
        <h4 style={{ margin: 0 }}>{name}</h4>
      </Grid>
      <Grid sx={{ border: 1 }} xs={2}>
        <h4 style={{ margin: 0 }}>{computerID}</h4>
      </Grid>
      <Grid
        sx={{
          display: "flex",
          alignItems: "center",
          justifyContent: "center",
        }}
        size="small"
        xs={2}
      >
        <IconButton
          style={{
            display: "block",
            margin: "auto",
          }}
          color="error"
          aria-label="delete"
          onClick={() => deleteFunc(itemID)}
        >
          <DeleteIcon />
        </IconButton>
      </Grid>
    </Grid>
  );
};

export default QueueItem;
