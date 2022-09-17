import React, { useState } from "react";
import QueueItem from "./QueueItem";
import { Stack, Container, TextField, Button } from "@mui/material";
import Grid from "@mui/material/Unstable_Grid2";
const Queue = () => {
  const [items, setItems] = useState([
    ["Ethan", 1],
    ["Adeline", 24],
    ["Jack", 11],
  ]);
  const [name, setName] = useState("");

  const addToQueue = () => {
    // TODO request to add to server
    // server returns the next available pc
    const computerID = 1;

    // success then add item to queue locally
    setItems([...items, [name, computerID]]);
    setName("");
  };

  const removeFromQueue = (itemID) => {
    // TODO request to remove item from server
    // success then remove item from queue locally
    setItems(items.filter((item, i) => i !== itemID));
  };

  return (
    <Stack sx={{ border: 1, borderRadius: "10px" }}>
      <Grid container>
        <Grid sx={{ borderBottom: 1 }} xs={8}>
          <h3>Name</h3>
        </Grid>
        <Grid sx={{ borderBottom: 1 }} xs={2}>
          <h3>ID</h3>
        </Grid>
        <Grid sx={{ borderBottom: 1 }} xs={2}></Grid>
      </Grid>
      <Container>
        <Stack sx={{ my: 1 }}>
          <TextField
            required
            id="name-input"
            label="Name"
            variant="outlined"
            value={name}
            onChange={(event) => {
              setName(event.target.value);
            }}
          />
          <Button variant="contained" onClick={addToQueue}>
            Add to Queue
          </Button>
        </Stack>
      </Container>
      <Container sx={{ my: 1, maxHeight: 200, overflow: "auto" }}>
        {items.map((item, i) => (
          <QueueItem
            name={item[0]}
            computerID={item[1]}
            key={i}
            itemID={i}
            deleteFunc={removeFromQueue}
          ></QueueItem>
        ))}
      </Container>
    </Stack>
  );
};

export default Queue;
