import React, { useEffect, useState } from "react";
import QueueItem from "./QueueItem";
import { Stack, Container, TextField, Button } from "@mui/material";
import Grid from "@mui/material/Unstable_Grid2";
import axios from "axios";
const Queue = ({ compStatusChange, setCompStatusChange }) => {
  const [items, setItems] = useState([]);
  const [firstname, setFirstName] = useState("");
  const [lastname, setLastInitial] = useState("");

  // Load initial queue items
  useEffect(() => {
    if (!compStatusChange) return;
    axios
      .get("/api/openrec/availability")
      .then((response) => {
        const nextAvailableIDs = response.data;

        axios
          .get("/api/openrec/queue")
          .then((response) => {
            const data = response.data;

            // success then add item to queue locally
            const newItems = [];
            for (let i = 0; i < data.length; i++) {
              newItems.push([
                data[i]["name"],
                nextAvailableIDs[i],
                data[i]["id"],
              ]);
            }
            setItems(newItems);
            setFirstName("");
            setLastInitial("");
          })
          .catch((error) => {
            if (error.response) {
              console.log(error.response);
            }
          });
      })
      .catch((error) => {
        if (error.response) {
          console.log(error.response);
        }
      });
    setCompStatusChange(false);
  }, [compStatusChange]);

  const addToQueue = () => {
    // TODO request to add to server
    // server returns the next available pc
    axios
      .get("/api/openrec/availability", {
        headers: {
          Authorization: "Bearer " + localStorage.getItem("jwt"),
        },
      })
      .then((response) => {
        const nextAvailableIDs = response.data;

        axios
          .post(
            "/api/openrec/queue",
            {
              first_name: firstname,
              last_name: lastname,
            },
            {
              headers: {
                Authorization: "Bearer " + localStorage.getItem("jwt"),
              },
            }
          )
          .then((response) => {
            const data = response.data;
            if (!data["success"]) return;
            const name = data["name"];
            const queueID = data["id"];

            // success then add item to queue locally
            const newItems = [];
            for (let i = 0; i < items.length; i++) {
              newItems.push([items[i][0], nextAvailableIDs[i], items[i][2]]);
            }
            setItems([
              ...newItems,
              [
                name,
                nextAvailableIDs[items.length === 0 ? 0 : items.length],
                queueID,
              ],
            ]);
            setFirstName("");
            setLastInitial("");
          })
          .catch((error) => {
            if (error.response) {
              console.log(error.response);
            }
          });
      })
      .catch((error) => {
        if (error.response) {
          console.log(error.response);
        }
      });
  };

  const removeFromQueue = (itemID) => {
    // TODO request to remove item from server
    axios
      .get("/api/openrec/availability", {
        headers: {
          Authorization: "Bearer " + localStorage.getItem("jwt"),
        },
      })
      .then((response) => {
        const nextAvailableIDs = response.data;

        axios
          .delete(`/api/openrec/queue/${itemID}`, {
            headers: {
              Authorization: "Bearer " + localStorage.getItem("jwt"),
            },
          })
          .then((response) => {
            const data = response.data;
            if (!data["success"]) return;

            const newItems = items.filter((item, i) => item[2] !== itemID);

            for (let i = 0; i < newItems.length; i++) {
              newItems[i] = [
                newItems[i][0],
                nextAvailableIDs[i],
                newItems[i][2],
              ];
            }

            // success then remove item from queue locally
            setItems(newItems);
          })
          .catch((error) => {
            if (error.response) {
              console.log(error.response);
            }
          });
      })
      .catch((error) => {
        if (error.response) {
          console.log(error.response);
        }
      });
  };

  return (
    <Stack sx={{ border: 1, borderRadius: "10px" }}>
      <Container>
        <Stack sx={{ my: 1 }}>
          <Grid container>
            <Grid xs={6}>
              <TextField
                required
                id="firstname-input"
                label="First"
                variant="outlined"
                value={firstname}
                onChange={(event) => {
                  setFirstName(event.target.value);
                }}
              />
            </Grid>
            <Grid xs={6}>
              <TextField
                required
                id="lastname-input"
                label="Last Initial"
                variant="outlined"
                value={lastname}
                inputProps={{ maxLength: 1 }}
                onChange={(event) => {
                  setLastInitial(event.target.value);
                }}
              />
            </Grid>
          </Grid>

          <Button variant="contained" onClick={addToQueue}>
            Add to Queue
          </Button>
        </Stack>
      </Container>
      <Grid container>
        <Grid sx={{ borderBottom: 1 }} xs={8}>
          <h3>Name</h3>
        </Grid>
        <Grid sx={{ borderBottom: 1 }} xs={2}>
          <h3>PC</h3>
        </Grid>
        <Grid sx={{ borderBottom: 1 }} xs={2}></Grid>
      </Grid>
      <Container sx={{ my: 1, maxHeight: 200, overflow: "auto" }}>
        {items.map((item, i) => (
          <QueueItem
            name={item[0]}
            computerID={item[1]}
            key={i}
            itemID={item[2]}
            deleteFunc={removeFromQueue}
          ></QueueItem>
        ))}
      </Container>
    </Stack>
  );
};

export default Queue;
