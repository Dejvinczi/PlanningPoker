import { useEffect, useState, useRef } from 'react';
import { useRouter } from 'next/router';
import { Button } from 'primereact/button';
import { Toast } from 'primereact/toast';
import { DataTable } from 'primereact/datatable';
import { Column } from 'primereact/column';
import CopyUrl from '@/components/CopyUrl';
import { getWsRoomUrl } from '@/api/ws';

const Game = ({ isAdmin, roomId, voterId }) => {
  const [voteChoices, setVoteChoices] = useState([]);
  const [selectedValue, setSelectedValue] = useState(null);
  const [endGame, setEndGame] = useState(false);
  const [votes, setVotes] = useState([]);
  const router = useRouter();
  const toast = useRef(null);
  const ws = useRef(null);

  function capitalizeFirstLetter(string) {
    return string.charAt(0).toUpperCase() + string.slice(1);
  }

  useEffect(() => {
    ws.current = new WebSocket(getWsRoomUrl(roomId));

    ws.current.onopen = () => {
      console.log('Websocket connected:');
    };

    ws.current.onmessage = (event) => {
      const data = JSON.parse(event.data);

      if (data.error) {
        router.push('/');
        return;
      }

      switch (data.action) {
        case 'get_vote_choices':
          setVoteChoices(data.vote_choices);
          break;
        case 'message':
          showToast(data.code, capitalizeFirstLetter(data.code), data.message);
          break;
        case 'refresh_votes':
          setVotes(data.votes);
          break;
        case 'reveal_votes':
          showToast('success', 'Reveal votes', data.message);
          setVotes(data.votes);
          setEndGame(true);
          break;
        case 'reset_votes':
          showToast('success', 'Reset votes', data.message);
          setVotes(data.votes);
          setEndGame(false);
          setSelectedValue(null);
          break;
        default:
          console.log('Received unknown action:', data.action);
      }
    };

    return () => {
      ws.current.close();
    };
  }, [roomId, router]);

  const showToast = (type, title, detail) => {
    toast.current.show({
      severity: type,
      summary: title,
      detail: detail,
      life: 3000,
    });
  };

  const vote = (value) => {
    setSelectedValue(value);

    const voteData = {
      action: 'vote',
      vote_id: voterId,
      value: value,
    };

    ws.current.send(JSON.stringify(voteData));
  };

  const revealVotes = () => {
    const voteData = {
      action: 'reveal',
    };

    ws.current.send(JSON.stringify(voteData));
  };

  const resetVotes = () => {
    const voteData = {
      action: 'reset',
    };

    ws.current.send(JSON.stringify(voteData));
  };

  return (
    <div>
      <Toast ref={toast} />
      <div
        className='p-d-flex p-ai-center p-jc-center'
        style={{ height: '10vh', textAlign: 'center' }}
      >
        <h1>Planning Poker Game</h1>
        {isAdmin ? (
          <div>
            <Button
              label='Reveal'
              disabled={
                !votes.length ||
                !votes.every((vote) => vote.voted === true) ||
                endGame
              }
              onClick={() => revealVotes()}
            />
            <Button
              label='Reset'
              disabled={!endGame}
              onClick={() => resetVotes()}
            />
          </div>
        ) : (
          voteChoices.map((choice) => (
            <Button
              className={
                selectedValue == choice.value ? 'p-button-success' : ''
              }
              key={choice.value}
              label={choice.label}
              disabled={endGame}
              onClick={() => vote(choice.value)}
            />
          ))
        )}
      </div>

      <div>
        <h2>Votes</h2>
        <DataTable value={votes} tableStyle={{ minWidth: '50rem' }}>
          <Column field='voter' header='Voter'></Column>
          <Column
            field='voted'
            header='Voted'
            body={(rowData) => (rowData.voted ? 'Yes' : 'No')}
          />
          <Column
            field='value'
            header='Value'
            body={(rowData) => (rowData.value ? rowData.value : 'Hidden')}
          />
        </DataTable>
      </div>
      <br />

      <div
        style={{
          display: 'flex',
          alignItems: 'center',
          justifyContent: 'space-between',
        }}
      >
        <Button
          label='Back'
          className='p-button-error'
          onClick={() => router.push('/')}
        />
        <CopyUrl
          url={window.location.origin + router.asPath}
          toastRef={toast}
        />
      </div>
    </div>
  );
};

export default Game;
