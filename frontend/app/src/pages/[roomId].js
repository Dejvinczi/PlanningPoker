import { useRouter } from 'next/router';
import { Button } from 'primereact/button';

export default function Room() {
  const router = useRouter();
  const { roomId } = router.query;

  return (
    <div>
      <h1>Room ID: {roomId}</h1>
      {/* There will be game logic */}
      <Button label='Back' onClick={() => router.push('/')} />
    </div>
  );
}
